SELECT
    *
FROM
    {{ ref("intermediate__job_contracts") }} jc1
JOIN
    {{ ref("intermediate__job_contracts") }} jc2
ON
        jc1.freelancer_sk = jc2.freelancer_sk
    AND jc1.sk != jc2.sk
    AND (
            (jc1.end_date IS NULL AND jc2.end_date IS NULL) -- We can't have to job contracts active at the same time
        OR  IF(jc2.end_date IS NULL, jc1.start_date >= jc2.start_date, jc1.start_date BETWEEN jc2.start_date AND jc2.end_date)
        OR  IF(jc2.end_date IS NULL, jc1.end_date >= jc2.start_date, jc1.end_date BETWEEN jc2.start_date AND jc2.end_date)
    )
ORDER BY
    COALESCE(jc1.freelancer_sk, jc2.freelancer_sk)