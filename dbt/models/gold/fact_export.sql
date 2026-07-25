{{ config(materialized='table') }}

WITH mapped_export AS (

    SELECT
        e.trade_year,
        e.trade_month,

        COALESCE(
            reporter_map.standard_country,
            e.reporter_country
        ) AS reporter_country,

        COALESCE(
            partner_map.standard_country,
            e.partner_country
        ) AS partner_country,

        e.commodity_code,
        e.net_weight_kg,
        e.trade_value_usd,

        COALESCE(reporter_map.is_active, TRUE) AS reporter_is_active,
        COALESCE(partner_map.is_active, TRUE) AS partner_is_active

    FROM {{ ref('silver_export') }} e

    LEFT JOIN {{ ref('country_mapping') }} reporter_map
        ON TRIM(e.reporter_country) = TRIM(reporter_map.raw_country)

    LEFT JOIN {{ ref('country_mapping') }} partner_map
        ON TRIM(e.partner_country) = TRIM(partner_map.raw_country)
)

SELECT
    d.date_key,

    reporter.country_key AS reporter_country_key,

    partner.country_key AS partner_country_key,

    commodity.commodity_key,

    e.net_weight_kg,

    e.trade_value_usd

FROM mapped_export e

INNER JOIN {{ ref('dim_date') }} d
    ON e.trade_year = d.year
   AND e.trade_month = d.month_number

INNER JOIN {{ ref('dim_country') }} reporter
    ON e.reporter_country = reporter.country_name

INNER JOIN {{ ref('dim_country') }} partner
    ON e.partner_country = partner.country_name

INNER JOIN {{ ref('dim_commodity') }} commodity
    ON e.commodity_code = commodity.commodity_code

WHERE e.reporter_is_active = TRUE
  AND e.partner_is_active = TRUE