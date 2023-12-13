{{ config(
    alias="app__invoices",
) }}


SELECT
    i.*
FROM
    {{ source("app", "invoices") }} i