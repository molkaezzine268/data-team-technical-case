{{ config(
    alias="kpi__monthly_turnover",
) }}


-- FIXME: DAT-04
SELECT
    date_trunc('month', i.issue_date) AS issue_month_date,
    SUM(i.amount) AS amount
FROM
    {{ ref("intermediate__invoices") }} i
GROUP BY
    date_trunc('month', i.issue_date)
    
WITH date_spine AS (
  SELECT DISTINCT
    generate_series(
      (SELECT MIN(date_trunc('month', issue_date)) FROM {{ ref("intermediate__invoices") }}),
      (SELECT MAX(date_trunc('month', issue_date)) FROM {{ ref("intermediate__invoices") }}),
      INTERVAL '1 month' #mois d'actobte manquant
    ) AS issue_month_date
)

SELECT
  d.issue_month_date,
  COALESCE(SUM(i.amount), 0) AS amount
FROM
  date_spine d
LEFT JOIN
  {{ ref("intermediate__invoices") }} i
ON
  date_trunc('month', i.issue_date) = d.issue_month_date
GROUP BY
  d.issue_month_date
ORDER BY
  d.issue_month_date;
