{{ config(materialized='table') }}

SELECT

    d.date_key,

    c.country_key,

    p.production_ktons,

    p.reserves_ktons,

    p.source_report,

    p.status

FROM {{ ref('silver_production') }} p

INNER JOIN {{ ref('dim_date') }} d
    ON p.production_year = d.year
   AND d.month_number = 1

INNER JOIN {{ ref('dim_country') }} c
    ON p.country = c.country_name