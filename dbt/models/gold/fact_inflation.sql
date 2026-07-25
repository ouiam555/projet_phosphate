{{ config(materialized='table') }}

SELECT

    d.date_key,

    c.country_key,

    i.inflation_rate

FROM {{ ref('silver_inflation') }} i

INNER JOIN {{ ref('dim_date') }} d
    ON i.inflation_year = d.year
   AND d.month_number = 1

INNER JOIN {{ ref('dim_country') }} c
    ON i.country = c.country_name