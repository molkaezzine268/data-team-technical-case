{{ config(
    alias="kpi__monthly_turnover",
) }}

SELECT
    date_trunc('month', i.issue_date) AS issue_month_date,
    SUM(i.amount) AS amount
FROM
    {{ ref("intermediate__invoices") }} i
GROUP BY
    date_trunc('month', i.issue_date)
