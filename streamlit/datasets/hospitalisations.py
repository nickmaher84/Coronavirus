import streamlit as st
from datasets._windows import rolling_metric_columns
from utils.db import fetch_query

HOSPITALISATION_METRICS = [
    "isolating_at_home",
    "hospitalised",
    "recovering_with_symptoms",
    "in_intensive_care",
    "entering_intensive_care",
    "leaving_intensive_care",
]


@st.cache_data(ttl=3600)
def national_hospitalisations():
    cols = rolling_metric_columns(HOSPITALISATION_METRICS, alias="h")
    query = f"""
            select
                date(h.date) as date,
                {cols}
            from
                italy.national_hospitalisations h
            window
                date_partition as (order by h.date),
                smoothed as (order by h.date range between interval 6 days preceding and current row)
            order by
                h.date"""
    return fetch_query(query)


@st.cache_data(ttl=3600)
def regional_hospitalisations():
    cols = rolling_metric_columns(HOSPITALISATION_METRICS, alias="h")
    query = f"""
            select
                h.region_code,
                dim.region_name,
                date(h.date) as date,
                {cols}
            from
                italy.regional_hospitalisations h
            join
                italy.region dim on dim.region_code = h.region_code
            window
                date_partition as (partition by h.region_code order by h.date),
                smoothed as (partition by h.region_code order by h.date range between interval 6 days preceding and current row)
            order by
                h.region_code, h.date"""
    return fetch_query(query)
