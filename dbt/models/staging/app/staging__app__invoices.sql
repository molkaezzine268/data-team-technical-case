{{ config(
    alias="app__invoices",
) }}


SELECT
    i.id,
    i.job_contract_id,
    i.client_id,
    i.reference,
    i.issue_date,
    CAST(i.amount AS DECIMAL(10, 2)) AS amount
FROM
    {{ source("app", "invoices") }} i