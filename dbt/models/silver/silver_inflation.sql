{{ config(materialized='table') }}

SELECT DISTINCT

    country,

    country_code,

    inflation_year,

    inflation_rate

FROM {{ ref('stg_inflation') }}

WHERE inflation_year BETWEEN 2016 AND 2026