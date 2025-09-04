from civis_backend_policy_analyser.models.assessment_area_summary import AssessmentAreaSummary
from civis_backend_policy_analyser.schemas.prompt_score_schema import PromptScoreEvaluationSchema, PromptScoreEvaluationSchema, PromptScoreSchema, PromptScoreSchemaOut
from civis_backend_policy_analyser.views.base_view import BaseView
from civis_backend_policy_analyser.models.prompt_score import PromptScore

from typing import List
from sqlalchemy import select
from sqlalchemy.orm import aliased
from civis_backend_policy_analyser.config.logging_config import logger
from civis_backend_policy_analyser.models.prompt import Prompt

class PromptScoreEvaluationView(BaseView):
    model = PromptScore
    schema = PromptScoreEvaluationSchema

    async def get_prompt_scores(self, doc_summary_id: int) -> List[PromptScoreEvaluationSchema]:
        
        logger.info(f"Fetching prompt scores for document summary id: {doc_summary_id}")

        aas = aliased(AssessmentAreaSummary)
        ps = aliased(PromptScore)
        p = aliased(Prompt)

        query = (
            select(
                aas.assessment_id,
                ps.prompt_id,
                p.criteria,
                ps.prompt_score,
                ps.max_score
            )
            .join(ps, aas.assessment_summary_id == ps.assessment_summary_id)
            .join(p, ps.prompt_id == p.prompt_id)
            .where(aas.doc_summary_id == doc_summary_id)
        )

        result = await self.db_session.execute(query)
        rows = result.mappings().all()
        logger.info(f"Fetched {len(rows)} prompt scores for document summary id: {doc_summary_id}")

        # Convert to PromptScoreEvaluationSchema
        return [PromptScoreEvaluationSchema.model_validate(prompt) for prompt in rows]


    