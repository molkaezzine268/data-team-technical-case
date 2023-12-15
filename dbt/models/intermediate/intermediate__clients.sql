{{ config(
    alias="clients",
) }}


SELECT
    b.*
FROM
    {{ ref("intermediate__base__clients") }} b