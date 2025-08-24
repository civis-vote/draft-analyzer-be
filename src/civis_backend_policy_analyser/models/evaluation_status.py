from enum import Enum

class EvaluationStatus(str, Enum):
    UPLOADED = "uploaded"
    VALIDATED = "validated"
    SUMMARIZED = "summarized"
    EVALUATED = "evaluated"
    SCORED = "scored"
    EXECUTIVE_SUMMARIZED = "executive_summarized"
    DOWNLOADED = "downloaded"