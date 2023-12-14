WITH
    invoices
AS (
    SELECT
        SUM(amount) AS amount
    FROM
        {{ ref("intermediate__invoices") }}
), 
    turnover
AS (
    SELECT
        SUM(amount) AS amount
    FROM
        {{ ref("marts__kpi__monthly_turnover") }}
)
SELECT
    *
FROM
    invoices i,
    turnover t
WHERE
    i.amount != t.amount