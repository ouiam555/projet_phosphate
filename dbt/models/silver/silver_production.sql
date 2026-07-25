{{ config(materialized='table') }}

SELECT DISTINCT

    production_year,

    country,

    production_ktons,

    reserves_ktons,

    source_report,

    status

FROM {{ ref('stg_production') }}

WHERE production_year BETWEEN 2016 AND 2026
  AND production_ktons > 0