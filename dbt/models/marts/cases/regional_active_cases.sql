select
    date,
    region_code,
    total_cases,
    total_recovered,
    total_deaths,
    active_cases,
    new_cases,
    new_recovered,
    new_deaths,
    change_in_active_cases,
    notes_on_cases,
    notes
from
    {{ ref('stg_regional_data') }}
