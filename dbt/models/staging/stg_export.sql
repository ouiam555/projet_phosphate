{{ config(materialized='view') }}

SELECT

    refYear AS trade_year,

    refMonth AS trade_month,

    TRIM(reporterISO) AS reporter_iso,
    TRIM(reporterDesc) AS reporter_country,

    TRIM(partnerISO) AS partner_iso,
    TRIM(partnerDesc) AS partner_country,

    TRIM(flowDesc) AS trade_flow,

    cmdCode AS commodity_code,
    TRIM(cmdDesc) AS commodity_description,

    netWgt AS net_weight_kg,

    primaryValue AS trade_value_usd

FROM {{ source('bronze', 'EXPORT_RAW') }}