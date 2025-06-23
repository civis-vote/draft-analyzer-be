DEFAULT_DRIVER = "asyncpg"  # Async Postgres Driver for master tables.
VECTOR_DRIVER = "psycopg"  # Langchain Postgres Driver
DB_BASE_URL = (
    'postgresql+{driver_name}://ffg:ffg_jpmc_civis@localhost:5432/civis'
)

AZURE_DEEPSEEK_API_KEY=""  ## TODO: Need to update this with actual
AZURE_DEEPSEEK_ENDPOINT="https://{resource}.services.ai.azure.com/models"  ## TODO: Need to update this with actual
AZURE_DEEPSEEK_MODEL="text-embedding-3-large"

POSTGRES_CONNECTION_STRING = DB_BASE_URL.format(driver_name=DEFAULT_DRIVER)
## TODO: Once confirms with `asyncpg` driver, will remove this connection string.
VECTOR_CONNECTION_STRING = DB_BASE_URL.format(driver_name=VECTOR_DRIVER)