{{ config(materialized='table') }}

WITH countries AS (

    SELECT country
    FROM {{ ref('silver_production') }}

    UNION

    SELECT country
    FROM {{ ref('silver_inflation') }}

    UNION

    SELECT reporter_country AS country
    FROM {{ ref('silver_import') }}

    UNION

    SELECT partner_country AS country
    FROM {{ ref('silver_import') }}

    UNION

    SELECT reporter_country AS country
    FROM {{ ref('silver_export') }}

    UNION

    SELECT partner_country AS country
    FROM {{ ref('silver_export') }}

),

mapped_countries AS (

    SELECT

        c.country AS raw_country,

        COALESCE(
            m.standard_country,
            c.country
        ) AS country_name,

        COALESCE(
            m.is_active,
            TRUE
        ) AS is_active

    FROM countries c

    LEFT JOIN {{ ref('country_mapping') }} m

        ON TRIM(c.country)=TRIM(m.raw_country)

)

SELECT DISTINCT

    HASH(country_name) AS country_key,

    country_name

FROM mapped_countries

WHERE is_active = TRUE
AND country_name IS NOT NULL

ORDER BY country_name
