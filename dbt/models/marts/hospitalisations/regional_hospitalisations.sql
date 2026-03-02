select
    date,
    region_code,
    active_cases,
    isolating_at_home,
    hospitalised,
    recovering_with_symptoms,
    in_intensive_care,
    entering_intensive_care,
    leaving_intensive_care,
    notes_on_cases,
    notes
from
    {{ ref('stg_regional_data') }}
