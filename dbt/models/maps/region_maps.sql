select
    reg_istat_code  as region_code,
    geom            as geometry
from {{ source('openpolis', 'regions') }}
