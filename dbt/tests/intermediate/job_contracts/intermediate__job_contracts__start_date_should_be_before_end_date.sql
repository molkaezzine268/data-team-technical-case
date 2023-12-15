SELECT
    *
FROM
    {{ ref("intermediate__job_contracts") }} jc
WHERE
        jc.end_date IS NOT NULL
    AND jc.end_date < jc.start_date