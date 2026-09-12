import os

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import sessionmaker

def get_database_url() -> str:
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    database = os.getenv("DB_NAME", "warehouse_sorter")
    user = os.getenv("DB_USER", "postgres")
    password = os.environ["DB_PASSWORD"]

    return (
        f"postgresql+psycopg://{user}:{password}"
        f"@{host}:{port}/{database}"
    )


engine: Engine = create_engine(get_database_url())

SessionFactory = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)