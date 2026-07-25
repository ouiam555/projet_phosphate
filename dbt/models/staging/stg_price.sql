{{ config(materialized='view') }}

SELECT

    TRY_TO_DATE(year || '-' || month || '-01', 'YYYY-MON-DD') AS price_date,

    price_usd_per_metric_ton AS phosphate_price_usd

FROM {{ source('bronze', 'PRICE_RAW') }}