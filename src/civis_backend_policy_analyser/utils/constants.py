import os

from dotenv import load_dotenv
from loguru import logger

load_dotenv()


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

logger.info(f"All environment variables loaded successfully.")