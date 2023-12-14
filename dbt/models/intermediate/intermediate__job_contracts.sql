{{ config(
    alias="job_contracts",
) }}


SELECT
    b.*
FROM
    {{ ref("intermediate__base__job_contracts") }} b