{% test equals_sum_of_columns(model, column_name, columns) %}
SELECT *
FROM {{ model }}
WHERE {{ column_name }} != {{ columns | join(' + ') }}
{% endtest %}
