-- Illustrative least-privilege pattern; review with Snowflake administrator.
-- Execute only with an appropriately privileged role in a NON-PRODUCTION account.
CREATE ROLE IF NOT EXISTS COPILOT_READONLY_ROLE;
GRANT USAGE ON DATABASE REBATE_ANALYTICS TO ROLE COPILOT_READONLY_ROLE;
GRANT USAGE ON SCHEMA REBATE_ANALYTICS.GOLD TO ROLE COPILOT_READONLY_ROLE;

-- Add SELECT grants only to reviewed views/semantic objects:
-- GRANT SELECT ON VIEW REBATE_ANALYTICS.GOLD.VW_REBATE_SUMMARY
--   TO ROLE COPILOT_READONLY_ROLE;

-- Do NOT grant access to BRONZE, SILVER, or RESTRICTED_DATA to the copilot role.
-- This script intentionally grants no base-table SELECT access.
