{{ config(
    alias="kpi__monthly_turnovers",
) }}

SELECT
    i.job_contract_id,
    SUM(i.amount) AS amount
FROM
    {{ ref("intermediate__invoices") }} i
GROUP BY
    i.job_contract_id
