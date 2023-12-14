{{ config(
    alias="app__users",
) }}


SELECT
    u.*
FROM
    {{ source("app", "users") }} u