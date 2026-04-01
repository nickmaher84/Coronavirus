import duckdb
from functools import lru_cache

@lru_cache(maxsize=1)
def get_connection():
    return duckdb.connect('../dbt/coronavirus.duckdb')

def fetch_query(query: str):
    conn = get_connection()
    return conn.execute(query).fetch_df()
