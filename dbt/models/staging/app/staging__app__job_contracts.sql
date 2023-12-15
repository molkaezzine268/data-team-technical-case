{{ config(
    alias="app__job_contracts",
) }}


SELECT
    jc.*
FROM
    {{ source("app", "job_contracts") }} jc