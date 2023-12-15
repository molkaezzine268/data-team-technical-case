{{ config(
    alias="invoices",
) }}


SELECT
    b.*
FROM
    {{ ref("intermediate__base__invoices") }} b