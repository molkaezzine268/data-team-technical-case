SELECT
    ANY_VALUE({{ dbt_utils.generate_surrogate_key([
        "c.name",
    ]) }}) AS sk,
    c.name,
    { app: { client_ids: array_agg(c.id) } } AS __
FROM
    {{ ref("staging__app__clients") }} c
GROUP BY
    c.name