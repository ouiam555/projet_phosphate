{{ config(materialized='table') }}

WITH mapped_import AS (

    SELECT
        i.trade_year,
        i.trade_month,

        COALESCE(
            reporter_map.standard_country,
            i.reporter_country
        ) AS reporter_country,

        COALESCE(
            partner_map.standard_country,
            i.partner_country
        ) AS partner_country,

        i.commodity_code,
        i.net_weight_kg,
        i.trade_value_usd,

        COALESCE(reporter_map.is_active, TRUE) AS reporter_is_active,
        COALESCE(partner_map.is_active, TRUE) AS partner_is_active

    FROM {{ ref('silver_import') }} i

    LEFT JOIN {{ ref('country_mapping') }} reporter_map
        ON TRIM(i.reporter_country) = TRIM(reporter_map.raw_country)

    LEFT JOIN {{ ref('country_mapping') }} partner_map
        ON TRIM(i.partner_country) = TRIM(partner_map.raw_country)
)

SELECT
    d.date_key,

    reporter.country_key AS reporter_country_key,

    partner.country_key AS partner_country_key,

    commodity.commodity_key,

    i.net_weight_kg,

    i.trade_value_usd

FROM mapped_import i

INNER JOIN {{ ref('dim_date') }} d
    ON i.trade_year = d.year
   AND i.trade_month = d.month_number

INNER JOIN {{ ref('dim_country') }} reporter
    ON i.reporter_country = reporter.country_name

INNER JOIN {{ ref('dim_country') }} partner
    ON i.partner_country = partner.country_name

INNER JOIN {{ ref('dim_commodity') }} commodity
    ON i.commodity_code = commodity.commodity_code

WHERE i.reporter_is_active = TRUE
  AND i.partner_is_active = TRUE