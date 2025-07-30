from civis_backend_policy_analyser.views.base_view import BaseView
from civis_backend_policy_analyser.models.document_score import DocumentScore
from civis_backend_policy_analyser.schemas.document_score_schema import DocumentScoreSchema, DocumentScoreOut, PromptScoreSchema

import json
import re
from typing import List
from datetime import datetime
from sqlalchemy import select
from loguru import logger
from civis_backend_policy_analyser.views.assessment_area_prompt_view import AssessmentAreaPromptView
from civis_backend_policy_analyser.models.prompt import Prompt
from civis_backend_policy_analyser.models.document_summary import DocumentSummary
from civis_backend_policy_analyser.schemas.prompt_schema import PromptSchema
from civis_backend_policy_analyser.schemas.assessment_area_summary_schema import AssessmentAreaSummarySchema
from civis_backend_policy_analyser.schemas.assessment_area_prompt_schema import AssessmentAreaPromptSchema
from civis_backend_policy_analyser.utils.constants import LLM_CLIENT
from civis_backend_policy_analyser.core.document_agent_factory import LLMClient, create_document_agent

class DocumentScoreView(BaseView):
    model = DocumentScore
    schema = DocumentScoreSchema
    
    async def score_assessment_area(self, doc_summary_id: int, assessment_id: int) -> List[DocumentScoreSchema]:
        # get the prompts associated with the current assessment_id
        prompt_records: List[PromptSchema] = await self.fetch_score_prompts(assessment_id)
        prompt_list = [prompt.technical_prompt for prompt in prompt_records]
        # fetch doc_id from document_summary table
        document_summary: DocumentSummary = await self.db_session.get(DocumentSummary, id=doc_summary_id)
        if not document_summary:
            raise ValueError(f"Document Summary with id {doc_summary_id} not found")
        document_id = document_summary.doc_id
        # assess the prompts from the LLM
        agent = create_document_agent(client=LLMClient(LLM_CLIENT), document_id=document_id)
        prompt_scores = agent.assess(prompt_list)
        if not prompt_scores:
            raise ValueError(f"Could not score prompts for document id: {document_id} under assessment id: {assessment_id}")
        logger.info(f"started fetching prompt scores from LLM for document id: {document_id} and assessment_id: {assessment_id}")
        # store the scores in document_score table
        assessment_scores = []
        for prompt in prompt_records:
            technical_prompt = prompt.technical_prompt
            '''
                LLM is expected to give the response for each prompt in below format that can be converted to json
                {
                    "prompt_score": 2.5,
                    "max_score": 5,
                    "score_justfication": "sample justification",
                    "reference": "sample reference"
                }
            '''
            llm_response_json = self._parse_llm_response(prompt_scores[technical_prompt])
            score_record = DocumentScore(
                doc_id = document_id,
                assessment_id = assessment_id,
                prompt_id = prompt.prompt_id,
                prompt_score = llm_response_json['prompt_score'],
                max_score = llm_response_json['max_score'],
                score_justification = llm_response_json['score_justification'],
                reference = llm_response_json['reference'],
                created_on = datetime.now(),
                created_by = "Admin"  # needs to be replaced with user_id
            )
            assessment_score = await self.create(score_record)
            assessment_scores.append(DocumentScoreSchema.model_validate(assessment_score))
        logger.info(f"completed scoring all prompts for document id: {document_id} and assessment id: {assessment_id}")
        return assessment_scores
    
    async def fetch_score_prompts(self, assessment_id: int) -> List[PromptSchema]:
        # get prompt ids from assessment_area_prompt table (mapping table)
        mapping_view = AssessmentAreaPromptView(self.db_session)
        mapping_records: List[AssessmentAreaPromptSchema] = await mapping_view.filter(assessment_id=assessment_id)
        if not mapping_records:
            raise ValueError(f"Prompts mapped to assessment area id {assessment_id} not found")
        prompt_ids = [record.prompt_id for record in mapping_records]
        # get the prompts for filtered prompt ids
        result = await self.db_session.execute(
            select(Prompt).where(Prompt.prompt_id.in_(prompt_ids))
        )
        prompt_objs = result.scalars().all()
        prompt_schema = PromptSchema()
        return [prompt_schema.from_orm(record) for record in prompt_objs]
    
    def _parse_llm_response(self, llm_response: str) -> dict:
        """Extract JSON object from LLM markdown-wrapped response."""
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", llm_response, re.DOTALL)
        json_str = match.group(1) if match else llm_response
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise ValueError("Invalid LLM response format")
    
    async def format_result(
            self, 
            assessment_area_summary: AssessmentAreaSummarySchema, 
            assessment_scores: List[DocumentScoreSchema]
        ) -> DocumentScoreOut:
        # variables to track total of prompt_score and max_score
        prompt_score_total = 0
        max_score_total = 0
        # create a list of PromptScoreSchema objs
        prompt_records = []
        for prompt_score in assessment_scores:
            prompt_score_total += prompt_score.prompt_score
            max_score_total += prompt_score.max_score
            prompt_record = PromptScoreSchema(
                prompt_id = prompt_score.prompt_id,
                score = prompt_score.prompt_score,
                justification = prompt_score.score_justification,
                reference = prompt_score.reference
            )
            prompt_records.append(prompt_record)
        # calculate score at assessment area level
        overall_score = prompt_score_total / max_score_total
        # create obj of DocumentScoreOut
        assessment_area_analysis = DocumentScoreOut(
            assessment_id = assessment_area_summary.assessment_id,
            summary = assessment_area_summary.summary_text,
            overall_score = overall_score,
            prompt_scores = prompt_records
        )
        return assessment_area_analysis
