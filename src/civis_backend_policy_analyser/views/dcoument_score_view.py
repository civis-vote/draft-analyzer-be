from civis_backend_policy_analyser.views.base_view import BaseView
from civis_backend_policy_analyser.models.document_score import DocumentScore
from civis_backend_policy_analyser.schemas.document_score_schema import DocumentScoreSchema

class DocumentScoreView(BaseView):
    model = DocumentScore
    schema = DocumentScoreSchema
    
    def score_assessment_area(self, document_id, assessment_id):
        
        # get assessment area details and prompts
        
        # iterative process to call LLM with document chunks and prompts

        # write the LLM json response to database

        # final response preparation 

        raise NotImplementedError
