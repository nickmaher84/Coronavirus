select
    date,
    country_code,
    total_cases,
    total_cases_from_diagnosis,
    total_cases_from_screening,
    new_cases,
    new_cases_from_diagnosis,
    new_cases_from_screening,
    notes_on_cases,
    notes
from
    {{ ref('stg_national_data') }}
where
    total_cases_from_screening is not null
