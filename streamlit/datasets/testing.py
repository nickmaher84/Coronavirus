import streamlit as st
from datasets._windows import rolling_metric_columns
from utils.db import fetch_query

TESTING_METRICS = [
    "new_tests",
    "new_molecular_tests",
    "new_rapid_antigen_tests",
    "new_cases_from_molecular_tests",
    "new_cases_from_rapid_antigen_tests",
]


@st.cache_data(ttl=3600)
def national_testing():
    cols = rolling_metric_columns(TESTING_METRICS, alias="t")
    query = f"""
            select
                date(t.date) as date,
                {cols}
            from
                italy.national_testing t
            window
                date_partition as (order by t.date),
                smoothed as (order by t.date range between interval 6 days preceding and current row)
            order by
                t.date"""
    return fetch_query(query)


@st.cache_data(ttl=3600)
def regional_testing():
    cols = rolling_metric_columns(TESTING_METRICS, alias="t")
    query = f"""
            select
                t.region_code,
                dim.region_name,
                date(t.date) as date,
                {cols}
            from
                italy.regional_testing t
            join
                italy.region dim on dim.region_code = t.region_code
            window
                date_partition as (partition by t.region_code order by t.date),
                smoothed as (partition by t.region_code order by t.date range between interval 6 days preceding and current row)
            order by
                t.region_code, t.date"""
    return fetch_query(query)
