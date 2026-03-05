{% test multicolumn_unique(model, columns) %}
SELECT {{ columns | join(', ') }}, COUNT()
FROM {{ model }}
GROUP BY {{ columns | join(', ') }}
HAVING COUNT() > 1
{% endtest %}
