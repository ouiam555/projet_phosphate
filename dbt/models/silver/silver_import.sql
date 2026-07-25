{{ config(materialized='table') }}

SELECT DISTINCT

    trade_year,
    trade_month,

    reporter_iso,
    reporter_country,

    partner_iso,
    partner_country,

    commodity_code,

    net_weight_kg,

    trade_value_usd

FROM {{ ref('stg_import') }}

WHERE trade_year BETWEEN 2016 AND 2026
  AND trade_value_usd > 0