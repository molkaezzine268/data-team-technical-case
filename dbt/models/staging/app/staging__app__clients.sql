{{ config(
    alias="app__clients",
) }}


SELECT
    c.*
FROM
    {{ source("app", "clients") }} c