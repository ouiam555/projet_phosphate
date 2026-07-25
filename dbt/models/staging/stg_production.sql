{{ config(materialized='view') }}

SELECT

    TRIM(PAYS) AS country,

    TRY_TO_NUMBER(LEFT(ANNEE, 4)) AS production_year,
    PRODUCTION_MILLIERS_TONNES AS production_ktons,

    RESERVES_MILLIERS_TONNES AS reserves_ktons,

    TRIM(SOURCE_RAPPORT) AS source_report,

    TRIM(STATUT) AS status

FROM {{ source('bronze', 'PRODUCTION_RAW') }}