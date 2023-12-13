{{ config(
    alias="invoices",
) }}


SELECT
    a.*
FROM
    {{ ref("staging__app__invoices") }} a