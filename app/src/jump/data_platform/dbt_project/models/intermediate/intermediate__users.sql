{{ config(
    alias="users",
) }}


SELECT
    u.*
FROM
    {{ ref("staging__app__users") }} u