import streamlit as st
from datasets._windows import rolling_metric_columns
from utils.db import fetch_query

SCREENING_METRICS = ["new_cases", "new_cases_from_diagnosis", "new_cases_from_screening"]


@st.cache_data(ttl=3600)
def national_screening():
    cols = rolling_metric_columns(SCREENING_METRICS, alias="s")
    query = f"""
            select
                date(s.date) as date,
                {cols}
            from
                italy.national_screening s
            window
                date_partition as (order by s.date),
                smoothed as (order by s.date range between interval 6 days preceding and current row)
            order by
                s.date"""
    return fetch_query(query)


@st.cache_data(ttl=3600)
def regional_screening():
    cols = rolling_metric_columns(SCREENING_METRICS, alias="s")
    query = f"""
            select
                s.region_code,
                dim.region_name,
                date(s.date) as date,
                {cols}
            from
                italy.regional_screening s
            join
                italy.region dim on dim.region_code = s.region_code
            window
                date_partition as (partition by s.region_code order by s.date),
                smoothed as (partition by s.region_code order by s.date range between interval 6 days preceding and current row)
            order by
                s.region_code, s.date"""
    return fetch_query(query)
