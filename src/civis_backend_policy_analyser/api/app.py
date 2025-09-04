from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from civis_backend_policy_analyser.api.history_router import history_router
from civis_backend_policy_analyser.api.report_generator_router import report_router
from civis_backend_policy_analyser.api.document_metadata_router import document_router
from civis_backend_policy_analyser.api.assessment_area_router import assessment_area_router
from civis_backend_policy_analyser.api.document_type_router import document_type_router
from civis_backend_policy_analyser.api.prompt_router import prompt_router
from civis_backend_policy_analyser.api.document_summary_router import summary_router
from civis_backend_policy_analyser.api.executive_summary_router import executive_summary_router
from civis_backend_policy_analyser.api.document_score_router import score_router
from civis_backend_policy_analyser.core.db_connection import sessionmanager
from civis_backend_policy_analyser.api.document_validate_router import validate_router
from civis_backend_policy_analyser.utils.constants import CORS_ORIGINS
from civis_backend_policy_analyser.config.logging_config import logger




@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, docs_url='/api/docs')

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/health-check')
async def root():
    logger.info("Health check endpoint hit")
    return {'message': 'Backend is running.'}


app.include_router(document_type_router)
app.include_router(assessment_area_router)
app.include_router(prompt_router)
app.include_router(document_router)
app.include_router(summary_router)
app.include_router(executive_summary_router)
app.include_router(score_router)
app.include_router(validate_router)
app.include_router(report_router)
app.include_router(history_router)


if __name__ == '__main__':
    uvicorn.run(
        'civis_backend_policy_analyser.api.app:app',
        host='0.0.0.0',
        reload=True,
        port=8000,
    )
