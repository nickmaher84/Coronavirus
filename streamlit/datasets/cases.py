import streamlit as st
from datasets._windows import rolling_metric_columns
from utils.db import fetch_query

CASE_METRICS = ["new_cases", "new_deaths", "new_recovered"]


@st.cache_data(ttl=3600)
def national_cases():
    query = """
            select
                date(date) as date,
                active_cases,
                lag(active_cases, 7) over date_partition  as active_cases_7d_ago,
                change_in_active_cases,
                new_cases,
                lag(new_cases, 7) over date_partition     as new_cases_7d_ago,
                avg(new_cases) over smoothed              as new_cases_7d_avg,
                new_deaths,
                lag(new_deaths, 7) over date_partition    as new_deaths_7d_ago,
                avg(new_deaths) over smoothed             as new_deaths_7d_avg,
                new_recovered,
                lag(new_recovered, 7) over date_partition as new_recovered_7d_ago,
                avg(new_recovered) over smoothed          as new_recovered_7d_avg
            from
                italy.national_active_cases
            window
                date_partition as (order by date),
                smoothed as (order by date range between interval 6 days preceding and current row)"""
    return fetch_query(query)


@st.cache_data(ttl=3600)
def regional_cases():
    cols = rolling_metric_columns(CASE_METRICS, alias="r")
    query = f"""
            select
                r.region_code,
                dim.region_name,
                date(r.date) as date,
                r.active_cases,
                lag(r.active_cases, 7) over date_partition as active_cases_7d_ago,
                r.change_in_active_cases,
                {cols}
            from
                italy.regional_active_cases r
            join
                italy.region dim on dim.region_code = r.region_code
            window
                date_partition as (partition by r.region_code order by r.date),
                smoothed as (partition by r.region_code order by r.date range between interval 6 days preceding and current row)
            order by
                r.region_code, r.date"""
    return fetch_query(query)


@st.cache_data(ttl=3600)
def province_cases():
    cols = rolling_metric_columns(["new_cases"], alias="p")
    query = f"""
            select
                p.province_code,
                dim.province_name,
                dim.region_code,
                date(p.date) as date,
                p.total_cases,
                {cols}
            from
                italy.province_cases p
            join
                italy.province dim on dim.province_code = p.province_code
            window
                date_partition as (partition by p.province_code order by p.date),
                smoothed as (partition by p.province_code order by p.date range between interval 6 days preceding and current row)
            order by
                p.province_code, p.date"""
    return fetch_query(query)
