select
    date,
    province_code,
    region_code,
    total_cases,
    new_cases,
    notes
from
    {{ ref('stg_province_data') }}
