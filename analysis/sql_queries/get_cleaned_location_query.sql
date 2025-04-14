SELECT 
    id,
    cleaned_location
FROM
    student.data_engineer_jobs
WHERE
    cleaned_location IS NOT NULL