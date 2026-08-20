def rolling_metric_columns(metrics, alias):
    """Build SQL select fragments for a list of metric column names, adding a
    7-days-ago lag and a 7-day trailing rolling average for each - mirrors the
    pattern used by hand in the original national_cases() query, so every
    domain gets rate-of-change columns without repeating the window logic.

    Expects named windows `date_partition` (order by date, optionally
    partitioned by grain) and `smoothed` (same, ranged over 6 preceding days)
    to be defined in the surrounding query's WINDOW clause.
    """
    parts = []
    for metric in metrics:
        parts.append(f"{alias}.{metric}")
        parts.append(f"lag({alias}.{metric}, 7) over date_partition as {metric}_7d_ago")
        parts.append(f"avg({alias}.{metric}) over smoothed as {metric}_7d_avg")
    return ",\n                ".join(parts)
