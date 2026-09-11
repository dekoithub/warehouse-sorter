import os
from typing import Any

import psycopg
from psycopg import Connection


def get_connection() -> Connection[tuple[Any, ...]]:
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "warehouse_sorter"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.environ["DB_PASSWORD"],
    )