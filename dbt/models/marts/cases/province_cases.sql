select
    date,
    province_code,
    total_cases,
    new_cases,
    notes
from
    {{ ref('stg_province_data') }}
