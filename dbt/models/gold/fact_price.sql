{{ config(materialized='table') }}

SELECT

    d.date_key,

    p.phosphate_price_usd

FROM {{ ref('silver_price') }} p

INNER JOIN {{ ref('dim_date') }} d
    ON p.price_date = d.full_date