from datetime import datetime
import os
from typing import List

from fastapi.responses import FileResponse
from loguru import logger
from sqlalchemy import select
from civis_backend_policy_analyser.models.assessment_area import AssessmentArea
from civis_backend_policy_analyser.models.assessment_area_summary import AssessmentAreaSummary
from civis_backend_policy_analyser.models.document_metadata import DocumentMetadata
from civis_backend_policy_analyser.models.document_summary import DocumentSummary
from civis_backend_policy_analyser.models.prompt import Prompt
from civis_backend_policy_analyser.models.prompt_score import PromptScore
from civis_backend_policy_analyser.report.generate_report import ReportGenerator
from civis_backend_policy_analyser.schemas.document_report_schema import CoverPageData, ReportRequest
from civis_backend_policy_analyser.schemas.document_summary_schema import DocumentReportOut
from civis_backend_policy_analyser.utils.constants import REPORTS_OUTPUT_DIR, REPORTS_TEMPLATE_DIR
from civis_backend_policy_analyser.views.base_view import BaseView

class DocumentReportView(BaseView):
    model = DocumentSummary
    schema = DocumentReportOut



    async def generate_document_report(self, doc_summary_id: int) -> DocumentReportOut:
        """
        Generate a report for the document with the given summary_id
        """
        
        # Initialize assessments list
        assessments: List[AssessmentArea] = []

        # Fetch the document summary to get doc_id and doc_type_id
        document_summary: DocumentSummary = await self.db_session.get(DocumentSummary, doc_summary_id)
        if not document_summary:
            raise ValueError(f"Invalid doc_summary_id: {doc_summary_id}")
        doc_id = document_summary.doc_id

        document_metadata: DocumentMetadata = await self.db_session.get(DocumentMetadata, doc_id)
        # Fetch assessment summaries for the document

        fetch_assessments_summary_stmt = select(AssessmentAreaSummary).where(
            AssessmentAreaSummary.doc_summary_id == doc_summary_id
        )
        assessments_summary_result = await self.db_session.execute(fetch_assessments_summary_stmt)
        assessment_summaries: list[AssessmentAreaSummary] = assessments_summary_result.scalars().all()

        if not assessment_summaries:
            raise ValueError(f"No assessment summaries found for doc_summary_id: {doc_summary_id}")
        
        index = 0
        for summary in assessment_summaries:
            assessment_id = summary.assessment_id
            assessment_summary_id = summary.assessment_summary_id
            index += 1

            assessment_area: AssessmentArea = await self.db_session.get(AssessmentArea, assessment_id)

            stmt = (
                select(PromptScore, Prompt)
                .join(Prompt, PromptScore.prompt_id == Prompt.prompt_id)
                .where(PromptScore.assessment_summary_id == assessment_summary_id)
            )
            result = await self.db_session.execute(stmt)
            score_rows = result.all()



            logger.info(f"Fetched score rows for assessment area {assessment_area.assessment_name} - {score_rows}")
            print(f"score_rows: {score_rows}")
            print(f"type of score_rows: {type(score_rows)}")
            # Append to assessments list
            assessments.append({
                "area_number": index,
                "title": assessment_area.assessment_name,
                "explanation": assessment_area.description,
                "scoring_table": [
                    {
                        "criterion": prompt.criteria,
                        "score": score.prompt_score,
                        "reasoning": score.score_justification,
                        "reference": score.reference
                    }
                    for score, prompt in score_rows
                    if score and prompt
                ],
                "summary": summary.summary_text
            })

        logger.info(f"Generated assessments for document {doc_id}: {assessments}")

        cover_data = {
                "report_title": "Draft Policy Analyser Report",
                "subtitle": f"Assessment for {document_metadata.file_name}",
                "date": datetime.now().strftime("%d %B %Y"),
                "submitted_to": "Directorate of Industries, Government of Maharashtra",
                "prepared_by": document_summary.created_by or "CIVIS"
            }

        generator = ReportGenerator(
            template_dir=REPORTS_TEMPLATE_DIR,
            output_dir=REPORTS_OUTPUT_DIR
        )
        request = ReportRequest(cover=CoverPageData(**cover_data), assessments=assessments)
        filename=f"policy_report_{doc_id}.pdf"
        report_path = generator.generate_combined_report(request=request, filename=filename)
        logger.info(f"Generated report at {report_path} for document {doc_id} with summary ID {doc_summary_id} and filename {filename}")

        document_summary.report_file_name = filename
        await self.db_session.commit()

        return DocumentReportOut(
            generated_report= report_path
        )

    async def download_report(self, doc_summary_id: int) -> FileResponse:
        """
        Download the report for the document with the given summary_id
        """
        document_summary: DocumentSummary = await self.db_session.get(DocumentSummary, doc_summary_id)
        if not document_summary:
            raise ValueError(f"Invalid doc_summary_id: {doc_summary_id}")

        report_file_name = document_summary.report_file_name
        if not report_file_name:
            logger.info(f"No report found. Generating new report for doc_summary_id: {doc_summary_id}")
            try:
                report_out : DocumentReportOut = await self.generate_document_report(doc_summary_id)
            except Exception as e:
                logger.error(f"Error generating report file name for doc_summary_id {doc_summary_id}: {e}")
        else:
            logger.info(f"Using existing report file name: {report_file_name}")
            report_out : DocumentReportOut = DocumentReportOut(
                generated_report=os.path.join(REPORTS_OUTPUT_DIR, report_file_name)
            )

        report_path = report_out.generated_report

        if not os.path.exists(report_path):
            raise FileNotFoundError(f"Report file not found at {report_path}")
        
        return FileResponse(
                path=str(report_path),
                filename=f"draft_policy_report_{doc_summary_id}.pdf",
                media_type="application/pdf"
            )