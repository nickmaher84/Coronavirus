{% test equals_sum_from_table(model, column_name, to, granularity) %}
WITH from_table AS (
    SELECT
        {{ granularity | join(', ') }},
        SUM({{ column_name }}) AS value
    FROM {{ model }}
    GROUP BY
        {{ granularity | join(', ') }}
),

to_table AS (
    SELECT
        {{ granularity | join(', ') }},
        SUM({{ column_name }}) AS value
    FROM {{ to }}
    GROUP BY
        {{ granularity | join(', ') }}
)

SELECT
    *
FROM from_table f
FULL JOIN to_table t
    USING ({{ granularity | join(', ') }})
WHERE f.value != t.value
OR f.value IS NULL
OR t.value IS NULL
{% endtest %}
