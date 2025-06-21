DEFAULT_DRIVER = "asyncpg"  # Async Postgres Driver for master tables.
VECTOR_DRIVER = "psycopg"  # Langchain Postgres Driver
DB_BASE_URL = (
    'postgresql+{driver_name}://ffg:ffg_jpmc_civis@localhost:5432/civis'
)

AZURE_DEEPSEEK_API_KEY=""
AZURE_DEEPSEEK_ENDPOINT="https://{resource}.services.ai.azure.com/models"
AZURE_DEEPSEEK_MODEL="text-embedding-3-large"
