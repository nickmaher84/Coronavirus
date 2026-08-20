select
    data                                   as date,
    stato                                  as country_code,
    codice_regione                         as region_code,
    denominazione_regione                  as region_name,
    codice_provincia                       as province_code,
    denominazione_provincia                as province_name,
    sigla_provincia                        as province_identifier,
    lat                                    as latitude,
    long                                   as longitude,
    totale_casi                            as total_cases,
    note                                   as notes,
    codice_nuts_1                          as nuts1_code,
    codice_nuts_2                          as nuts2_code,
    codice_nuts_3                          as nuts3_code
from {{ source('pcm-dpc', 'province') }}
