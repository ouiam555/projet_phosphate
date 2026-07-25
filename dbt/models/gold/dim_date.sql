{{ config(materialized='table') }}

WITH date_spine AS (

    SELECT
        DATEADD(
            month,
            SEQ4(),
            TO_DATE('2016-01-01')
        ) AS full_date

    FROM TABLE(GENERATOR(ROWCOUNT => 132))

)

SELECT

    TO_NUMBER(TO_CHAR(full_date, 'YYYYMMDD')) AS date_key,

    full_date,

    YEAR(full_date) AS year,

    MONTH(full_date) AS month_number,

    MONTHNAME(full_date) AS month_name,

    QUARTER(full_date) AS quarter

FROM date_spine

WHERE full_date <= TO_DATE('2026-12-01')

ORDER BY full_date