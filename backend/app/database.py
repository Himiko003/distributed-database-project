import os
import time
import psycopg
from psycopg.types.json import Jsonb

def connect_with_retry(host: str, attempts: int = 20):
    last_error = None
    for _ in range(attempts):
        try:
            return psycopg.connect(
                host=host,
                port=os.getenv("DB_PORT", "5432"),
                dbname=os.getenv("DB_NAME", "sbdt_db"),
                user=os.getenv("DB_USER", "app_user"),
                password=os.getenv("DB_PASSWORD", "app_password_dev"),
                connect_timeout=5,
            )
        except Exception as exc:
            last_error = exc
            time.sleep(2)
    raise RuntimeError(f"Database {host} unavailable: {last_error}")

def write_inference(input_data: dict, predicted_class: str):
    with connect_with_retry(os.getenv("DB_WRITE_HOST", "localhost")) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO inference_history (input_data, predicted_class)
                   VALUES (%s, %s) RETURNING id, created_at""",
                (Jsonb(input_data), predicted_class),
            )
            row = cur.fetchone()
        conn.commit()
    return {"id": row[0], "created_at": row[1].isoformat()}

def read_history(limit: int = 20):
    with connect_with_retry(os.getenv("DB_READ_HOST", "localhost")) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT id, input_data, predicted_class, created_at
                   FROM inference_history ORDER BY id DESC LIMIT %s""",
                (limit,),
            )
            rows = cur.fetchall()
    return [
        {"id": r[0], "input_data": r[1], "predicted_class": r[2], "created_at": r[3].isoformat()}
        for r in rows
    ]
