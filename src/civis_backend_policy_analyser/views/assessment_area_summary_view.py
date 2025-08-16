from typing import List
from civis_backend_policy_analyser.models.prompt_score import PromptScore
from civis_backend_policy_analyser.schemas.prompt_score_schema import PromptScoreSchema
from civis_backend_policy_analyser.views.base_view import BaseView
from civis_backend_policy_analyser.models.assessment_area_summary import AssessmentAreaSummary
from civis_backend_policy_analyser.schemas.assessment_area_summary_schema import AssessmentAreaSummaryOut, AssessmentAreaSummarySchema

from sqlalchemy import select
from datetime import datetime
from loguru import logger
from civis_backend_policy_analyser.models.assessment_area import AssessmentArea
from civis_backend_policy_analyser.models.prompt import Prompt
from civis_backend_policy_analyser.models.document_summary import DocumentSummary
from civis_backend_policy_analyser.utils.constants import LLM_CLIENT
from civis_backend_policy_analyser.core.document_agent_factory import LLMClient, create_document_agent

class AssessmentAreaSummaryView(BaseView):
    model = AssessmentAreaSummary
    schema = AssessmentAreaSummarySchema

    async def summarize_assessment_area(self, doc_summary_id: int, assessment_id: int) -> AssessmentAreaSummarySchema:
        # fetch assessment area summary prompt
        summary_prompt = await self.fetch_summary_prompt(assessment_id)
        # fetch doc_id from document_summary table
        document_summary: DocumentSummary = await self.db_session.get(DocumentSummary, doc_summary_id)
        if not document_summary:
            raise ValueError(f"Document Summary with id {doc_summary_id} not found")
        document_id = document_summary.doc_id
        # create document agent and invoke LLM
        agent = create_document_agent(client=LLMClient(LLM_CLIENT), document_id=document_id)

        logger.info(f"started fetching summary from LLM for document id: {document_id} and assessment id: {assessment_id}")
        assessment_summary = agent.summarize(summary_prompt=summary_prompt)
        if not assessment_summary:
            raise ValueError(f"Could not summarize document {document_id} for assessment area {assessment_id}")
        
        summary_record = AssessmentAreaSummary(
            doc_summary_id = doc_summary_id,
            assessment_id = assessment_id,
            summary_text = assessment_summary,
            created_on = datetime.now(),
            created_by = "Admin"  # needs to be replaced with user_id
        )
        logger.info(f"fetched summary from LLM: {assessment_summary}")
        assessment_area_summary = await self.create(summary_record)
        return AssessmentAreaSummarySchema.model_validate(assessment_area_summary)

    async def fetch_summary_prompt(self, assessment_id: int) -> str:
        # get prompt id from summary_prompt column in assessment_area table
        assessment_area_record: AssessmentArea = await self.db_session.get(AssessmentArea, assessment_id)
        if not assessment_area_record:
            raise ValueError(f"Assessment area with id {assessment_id} not found")
        # get prompt for that id from the prompt table
        prompt_id = assessment_area_record.summary_prompt
        prompt_record: Prompt = await self.db_session.get(Prompt, prompt_id)
        if not prompt_record:
            raise ValueError(f"Prompt with id {prompt_id} not found")
        summary_prompt = prompt_record.technical_prompt
        return summary_prompt

    async def format_result(
            self, 
            assessment_area_summary: AssessmentAreaSummarySchema, 
            prompt_scores: List[PromptScoreSchema]
        ) -> AssessmentAreaSummaryOut:
        # variables to track total of prompt_score and max_score
        prompt_score_total = 0
        max_score_total = 0
        # create a list of PromptScoreSchema objs
        prompt_records = []
        for prompt_score in prompt_scores:
            prompt_score_total += prompt_score.prompt_score if prompt_score.prompt_score is not None else 0
            max_score_total += prompt_score.max_score if prompt_score.max_score is not None else 5
            prompt_records.append(prompt_score)

        if max_score_total == 0:
            logger.warning("Max score total is zero, setting overall score to 1.0 to avoid division by zero.")
            max_score_total =  1
        # calculate score at assessment area level (score out of 10)
        overall_score = (prompt_score_total / max_score_total) * 10
        
        logger.info(f"Overall score for assessment area {assessment_area_summary.assessment_id} is {overall_score}")

        # create obj of AssessmentAreaSummaryOut
        assessment_area_analysis = AssessmentAreaSummaryOut(
            assessment_summary_id = assessment_area_summary.assessment_summary_id,
            assessment_id = assessment_area_summary.assessment_id,
            summary = assessment_area_summary.summary_text,
            overall_score = overall_score,
            prompt_scores = prompt_records
        )
        return assessment_area_analysis

    async def get_existing_assessment_area_summary(self, doc_summary_id: int, assessment_id: int) -> AssessmentAreaSummaryOut:
        """
        Get the existing assessment area summary for the given document and assessment id to avoid LLM call for same request.
        """

        logger.info(f"Fetching existing assessment area summary for doc_summary_id: {doc_summary_id} and assessment_id: {assessment_id}")

        assessment_area_stmt = select(AssessmentAreaSummary).where(
            AssessmentAreaSummary.doc_summary_id == doc_summary_id,
            AssessmentAreaSummary.assessment_id == assessment_id
        )
        result = await self.db_session.execute(assessment_area_stmt)
        summary = result.scalars().first()
        if not summary:
            return None

        prompt_scores = await self.db_session.execute(
            select(PromptScore)
            .join(AssessmentAreaSummary, AssessmentAreaSummary.assessment_summary_id == PromptScore.assessment_summary_id)
            .where(
                AssessmentAreaSummary.doc_summary_id == doc_summary_id,
                AssessmentAreaSummary.assessment_id == assessment_id
            )
        )
        prompt_scores_schema = prompt_scores.scalars().all()
        if not prompt_scores_schema:
            logger.warning(f"No prompt scores found for doc_summary_id: {doc_summary_id} and assessment_id: {assessment_id}")
            return None
        
        format_result = await self.format_result(summary, prompt_scores_schema)
        logger.info(f"Fetched existing assessment area summary: {format_result}")

        return AssessmentAreaSummaryOut.model_validate(format_result)