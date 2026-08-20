select
    date,
    country_code,
    region_code,
    region_name,
    province_code,
    province_name,
    province_identifier,
    nuts1_code,
    nuts2_code,
    nuts3_code,
    latitude,
    longitude,

    total_cases,
    coalesce(lag(total_cases,  7) over province_data, 0)    as total_cases_1w_ago,
    coalesce(lag(total_cases, 14) over province_data, 0)    as total_cases_2w_ago,
    total_cases - coalesce(
        lag(total_cases) over province_data, 0
    )                                                       as new_cases,
    string_to_array(notes, ';')                             as notes
from
    {{ ref('provincial') }}
window
    province_data as (partition by province_code order by date)
