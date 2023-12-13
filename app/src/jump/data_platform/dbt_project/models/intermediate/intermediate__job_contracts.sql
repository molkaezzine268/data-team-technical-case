{{ config(
    alias="job_contracts",
) }}


SELECT
    a.*
FROM
    {{ ref("staging__app__job_contracts") }} a