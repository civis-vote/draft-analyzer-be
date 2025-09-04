import os

from dotenv import load_dotenv
from civis_backend_policy_analyser.config.logging_config import logger

load_dotenv()

CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_PATH = os.getenv("LOG_PATH", "")
LOG_ROTATION = os.getenv("LOG_ROTATION", "5 MB")
LOG_RETENTION = os.getenv("LOG_RETENTION", "7 days")
LOG_COMPRESSION = os.getenv("LOG_COMPRESSION", "zip")

# Database connection strings
DEFAULT_DRIVER = "asyncpg"
VECTOR_DRIVER = "psycopg"

DB_BASE_URL = (
    "postgresql+{driver_name}://{user}:{password}@{host}:{port}/{dbname}"
).format(
    driver_name="{driver_name}",
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=os.environ["DB_PORT"],
    dbname=os.environ["DB_NAME"],
)

POSTGRES_CONNECTION_STRING = DB_BASE_URL.format(driver_name=DEFAULT_DRIVER)
VECTOR_CONNECTION_STRING = DB_BASE_URL.format(driver_name=VECTOR_DRIVER)



# Environment variables for Azure DeepSeek
AZURE_DEEPSEEK_API_KEY = os.environ["AZURE_DEEPSEEK_API_KEY"]
AZURE_DEEPSEEK_ENDPOINT = os.environ["AZURE_DEEPSEEK_ENDPOINT"]
AZURE_DEEPSEEK_MODEL = os.environ["AZURE_DEEPSEEK_MODEL"]
AZURE_DEEPSEEK_DEPLOYMENT_NAME = os.environ["AZURE_DEEPSEEK_DEPLOYMENT_NAME"]
AZURE_OPENAI_API_VERSION = os.environ["AZURE_OPENAI_API_VERSION"]

LLM_CLIENT = os.environ.get("LLM_CLIENT", "ollama").lower()

REPORTS_TEMPLATE_DIR=os.environ.get("REPORTS_TEMPLATE_DIR", "templates")
REPORTS_OUTPUT_DIR=os.environ.get("REPORTS_OUTPUT_DIR", "reports")


logger.info(f"All environment variables loaded successfully.")