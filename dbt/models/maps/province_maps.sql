select
    prov_istat_code as province_code,
    geom            as geometry
from {{ source('openpolis', 'provinces') }}
