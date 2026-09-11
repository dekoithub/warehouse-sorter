from typing import Any

from infrastructure.database import get_connection


def get_all_destinations() -> list[tuple[Any, ...]]:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, code, name, is_active
                FROM destinations
                ORDER BY id;
                """
            )

            return cursor.fetchall()

def create_destination(code: int, name: str) -> None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO destinations (
                    code,
                    name
                )
                VALUES (%s, %s);
                """,
                (code, name),
            )

def get_destination_by_code(code: int) -> tuple[Any, ...] | None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, code, name, is_active
                FROM destinations
                WHERE code = %s;
                """,
                (code,),
            )

            return cursor.fetchone()