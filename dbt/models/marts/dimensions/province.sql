with
provinces as (
    select
        *,
        row_number() over (
            partition by province_code
            order by date desc
        ) as rn
    from
        {{ ref('stg_province_data') }}
)

select
    province_code,
    province_name,
    province_identifier,
    region_code,
    region_name,
    country_code,
    nuts1_code,
    nuts2_code,
    nuts3_code,
    latitude,
    longitude
from
    provinces
where
    rn = 1
