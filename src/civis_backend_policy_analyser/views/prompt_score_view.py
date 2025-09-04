from civis_backend_policy_analyser.schemas.prompt_score_schema import PromptScoreSchema
from civis_backend_policy_analyser.views.base_view import BaseView
from civis_backend_policy_analyser.models.prompt_score import PromptScore

import json
import re
from typing import List, Union
from datetime import datetime
from sqlalchemy import select
from civis_backend_policy_analyser.config.logging_config import logger
from civis_backend_policy_analyser.models.prompt import Prompt
from civis_backend_policy_analyser.models.document_summary import DocumentSummary
from civis_backend_policy_analyser.models.assessment_area_prompt import AssessmentAreaPrompt
from civis_backend_policy_analyser.schemas.prompt_schema import PromptSchema
from civis_backend_policy_analyser.schemas.assessment_area_summary_schema import AssessmentAreaSummarySchema
from civis_backend_policy_analyser.utils.constants import LLM_CLIENT
from civis_backend_policy_analyser.core.document_agent_factory import LLMClient, create_document_agent

class PromptScoreView(BaseView):
    model = PromptScore
    schema = PromptScoreSchema

    async def score_assessment_area(self, assessment_area_summary: AssessmentAreaSummarySchema) -> List[PromptScoreSchema]:

        assessment_summary_id = assessment_area_summary.assessment_summary_id
        assessment_id = assessment_area_summary.assessment_id
        # get the prompts associated with the current assessment_id
        prompt_records: List[PromptSchema] = await self.fetch_score_prompts(assessment_id)

        # fetch doc_id from document_summary table
        document_summary: DocumentSummary = await self.db_session.get(DocumentSummary, assessment_area_summary.doc_summary_id)
        if not document_summary:
            raise ValueError(f"Document Summary with id {assessment_area_summary.doc_summary_id} not found")
        document_id = document_summary.doc_id
        # assess the prompts from the LLM
        agent = create_document_agent(client=LLMClient(LLM_CLIENT), document_id=document_id)

        prompt_inputs = [
            {"prompt_id": prompt.prompt_id, "query": prompt.technical_prompt}
            for prompt in prompt_records
        ]
        logger.info(f"started fetching prompt scores from LLM for document id: {document_id} and assessment_id: {assessment_id}")
        prompt_scores_results = agent.assess(prompt_inputs)
        if not prompt_scores_results:
            raise ValueError(f"Could not score prompts for document id: {document_id} under assessment id: {assessment_id}")
        
        logger.info(f"fetched prompt scores from LLM for document id: {document_id} and assessment_id: {assessment_id} - {prompt_scores_results}")

        # parse the results from LLM
        prompt_answers = {
            item["prompt_id"]: result["result"]
            for item, result in zip(prompt_inputs, prompt_scores_results)
        }

        # store the scores in document_score table
        assessment_scores = []

        for prompt_id, llm_result in prompt_answers.items():
            
            llm_response_json = self._parse_llm_response(llm_result)

            score_record = PromptScoreSchema(
                assessment_summary_id=assessment_summary_id,
                prompt_id=prompt_id,
                prompt_score=llm_response_json.get('score'),
                max_score=llm_response_json.get('max_score'),
                score_justification=llm_response_json.get('reasoning'),
                reference=llm_response_json.get('ref'),
                created_on=datetime.now(),
                created_by="Admin"  # Replace with current user later
            )
            logger.info(f"Creating PromptScore record: {score_record}")
            assessment_score = await self.create(score_record)
            assessment_scores.append(PromptScoreSchema.model_validate(assessment_score))

        logger.info(f"completed scoring all prompts for document id: {document_id} and assessment id: {assessment_id}")
        return assessment_scores
    

    async def fetch_score_prompts(self, assessment_id: int) -> List[PromptSchema]:
        # 1. Get all prompt IDs mapped to the assessment
        result = await self.db_session.execute(
            select(AssessmentAreaPrompt.prompt_id).where(
                AssessmentAreaPrompt.assessment_id == assessment_id
            )
        )
        prompt_ids = result.scalars().all()

        if not prompt_ids:
            raise ValueError(f"No prompts mapped to assessment area id {assessment_id}")

        logger.info(f"Fetched prompt IDs for assessment area {assessment_id}: {prompt_ids}")

        # 2. Fetch full Prompt objects using the IDs
        prompt_result = await self.db_session.execute(
            select(Prompt).where(Prompt.prompt_id.in_(prompt_ids))
        )
        prompt_objs = prompt_result.scalars().all()

        # 3. Convert to PromptSchema
        return [PromptSchema.model_validate(prompt) for prompt in prompt_objs]

    
    # Helper method to parse LLM response

    def _parse_llm_response(self, llm_response: Union[str, dict]) -> dict:
        """Extract JSON object from LLM markdown-wrapped response or pass through if already a dict."""

        if isinstance(llm_response, dict):
            return llm_response  # Already parsed

        if not isinstance(llm_response, str):
            raise ValueError(f"Expected string or dict from LLM, got: {type(llm_response)}")

        # Extract JSON from triple backticks
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", llm_response, re.DOTALL)
        json_str = match.group(1) if match else llm_response

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}\nRaw response: {llm_response}")
            raise ValueError("Invalid LLM response format")

    
    