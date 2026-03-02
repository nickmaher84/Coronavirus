select
    date,
    country_code,
    region_code,
    region_name,
    nuts1_code,
    nuts2_code,
    latitude,
    longitude,

    coalesce(total_molecular_tests, total_tests)            as total_molecular_tests,
    coalesce(total_rapid_antigen_tests, 0)                  as total_rapid_antigen_tests,
    total_tests,

    coalesce(total_cases_from_molecular_tests, total_cases) as total_cases_from_molecular_tests,
    coalesce(total_cases_from_rapid_antigen_tests, 0)       as total_cases_from_rapid_antigen_tests,
    total_cases_tested,

    total_cases_from_diagnosis,
    total_cases_from_screening,

    total_cases,
    total_recovered,
    total_deaths,
    active_cases,

    isolating_at_home,
    hospitalised,
    recovering_with_symptoms,
    in_intensive_care,
    entering_intensive_care,
    entering_intensive_care + coalesce(
        lag(in_intensive_care) over region_data, 0
    ) - in_intensive_care                                   as leaving_intensive_care,

    coalesce(total_molecular_tests, total_tests) - coalesce(
        lag(coalesce(total_molecular_tests, total_tests)) over region_data, 0
    )                                                       as new_molecular_tests,
    coalesce(total_rapid_antigen_tests, 0) - coalesce(
        lag(total_rapid_antigen_tests) over region_data, 0
    )                                                       as new_rapid_antigen_tests,
    total_tests - coalesce(
        lag(total_tests) over region_data, 0
    )                                                       as new_tests,

    coalesce(total_cases_from_molecular_tests, total_cases) - coalesce(
        lag(coalesce(total_cases_from_molecular_tests, total_cases)) over region_data, 0
    )                                                       as new_cases_from_molecular_tests,
    coalesce(total_cases_from_rapid_antigen_tests, 0) - coalesce(
        lag(total_cases_from_rapid_antigen_tests) over region_data, 0
    )                                                       as new_cases_from_rapid_antigen_tests,
    total_cases_tested - coalesce(
        lag(total_cases_tested) over region_data, 0
    )                                                       as new_cases_tested,

    total_cases_from_diagnosis -
        lag(total_cases_from_diagnosis) over region_data
                                                            as new_cases_from_diagnosis,
    total_cases_from_screening -
        lag(total_cases_from_screening) over region_data
                                                            as new_cases_from_screening,
    new_cases,
    total_recovered - coalesce(
        lag(total_recovered) over region_data, 0
    )                                                       as new_recovered,
    total_deaths - coalesce(
        lag(total_deaths) over region_data, 0
    )                                                       as new_deaths,
    change_in_active_cases,

    notes_on_tests,
    notes_on_cases,
    string_to_array(notes, ';')                             as notes
from
    {{ ref('regional') }}
window
    region_data as (partition by region_code order by date)