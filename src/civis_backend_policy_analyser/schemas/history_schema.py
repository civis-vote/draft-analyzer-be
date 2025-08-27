from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class DocumentHistorySchema(BaseModel):
    doc_type_id: int
    doc_summary_id: int
    file_name: str
    summary_time: datetime
    status: Optional[str] = None
    doc_type: str

    model_config = {
        "from_attributes": True  
    }

class DocumentHistorySchemaOut(BaseModel):
    history: List[DocumentHistorySchema]