DEFAULT_DRIVER = "asyncpg"  # Async Postgres Driver for master tables.
VECTOR_DRIVER = "psycopg"  # Langchain Postgres Driver
DB_BASE_URL = (
    'postgresql+{driver_name}://ffg:ffg_jpmc_civis@localhost:5432/civis'
)
