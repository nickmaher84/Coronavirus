import duckdb
from functools import lru_cache
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent / "dbt" / "coronavirus.duckdb"

@lru_cache(maxsize=1)
def get_connection():
    conn = duckdb.connect(str(DB_PATH), read_only=True)
    conn.execute("install spatial; load spatial;")
    return conn

def fetch_query(query: str):
    conn = get_connection()
    return conn.execute(query).fetch_df()
