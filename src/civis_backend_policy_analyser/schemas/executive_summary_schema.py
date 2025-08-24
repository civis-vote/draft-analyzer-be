from pydantic import BaseModel

class ExecutiveSummarySchema(BaseModel):
    doc_summary_id: int
    executive_summary_text: str

    model_config = {
        "from_attributes": True  
    }
