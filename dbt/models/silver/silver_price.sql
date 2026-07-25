SELECT DISTINCT

    price_date,

    YEAR(price_date)  AS price_year,

    MONTH(price_date) AS price_month,

    phosphate_price_usd

FROM {{ ref('stg_price') }}

WHERE phosphate_price_usd > 0
  AND YEAR(price_date) BETWEEN 2016 AND 2026