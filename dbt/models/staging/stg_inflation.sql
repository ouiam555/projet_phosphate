{{ config(materialized='view') }}

SELECT

    TRIM(COUNTRY) AS country,

    TRIM(COUNTRY_CODE) AS country_code,

    YEAR AS inflation_year,

    INFLATION AS inflation_rate

FROM {{ source('bronze', 'INFLATION_RAW') }}