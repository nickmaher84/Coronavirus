with
regions as (
    select
        *,
        row_number() over (
            partition by region_code
            order by date desc
        ) as rn
    from
        {{ ref('stg_regional_data') }}
)

select
    region_code,
    region_name,
    country_code,
    nuts1_code,
    nuts2_code,
    latitude,
    longitude
from
    regions
where
    rn = 1
