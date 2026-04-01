import streamlit as st
from utils.db import fetch_query

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
