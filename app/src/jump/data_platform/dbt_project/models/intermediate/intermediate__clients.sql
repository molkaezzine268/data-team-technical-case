{{ config(
    alias="clients",
) }}


SELECT
    a.*
FROM
    {{ ref("staging__app__clients") }} a