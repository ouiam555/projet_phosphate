{{ config(materialized='table') }}

WITH commodities AS (

    SELECT
        commodity_code,
        commodity_description
    FROM {{ ref('stg_import') }}

    UNION

    SELECT
        commodity_code,
        commodity_description
    FROM {{ ref('stg_export') }}

)

SELECT DISTINCT

    HASH(commodity_code) AS commodity_key,

    commodity_code,

    TRIM(commodity_description) AS commodity_name

FROM commodities

WHERE commodity_code IS NOT NULL
  AND commodity_description IS NOT NULL

ORDER BY commodity_code