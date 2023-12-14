{{ config(
    alias="freelances",
) }}


SELECT
    b.*
FROM
    {{ ref("intermediate__base__freelances") }} b