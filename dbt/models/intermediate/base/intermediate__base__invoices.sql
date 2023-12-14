WITH
    client_mappings
AS (
    SELECT
        c.sk AS client_sk,
        a.__app__client_id
    FROM
        {{ ref("intermediate__base__clients") }} c,
        UNNEST(c.__.app.client_ids) AS a(__app__client_id)
)
SELECT
    {{ dbt_utils.generate_surrogate_key([
        "i.reference",
    ]) }} AS sk,
    jc.sk AS job_contract_sk,
    cm.client_sk,
    i.reference,
    i.issue_date,
    i.amount
FROM
    {{ ref("staging__app__invoices") }} i
LEFT JOIN
    {{ ref("intermediate__base__job_contracts") }} jc
ON
    jc.__.app.job_contract_id = i.job_contract_id
LEFT JOIN
    client_mappings cm
ON
    cm.__app__client_id = i.client_id