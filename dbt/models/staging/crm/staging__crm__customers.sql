{{ config(
    alias="crm__customers",
) }}


SELECT
    s.last_name,
    s.first_name,
    s.email,
    s.satisfaction_score
FROM
    {{ source("crm", "customers") }} s