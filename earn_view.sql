CREATE VIEW EARNING_VIEW AS
SELECT date::DATE as Date,
      date::TIME as TIME,
      country,
      company,
      short_code,

      CASE
        WHEN eps_actual <> '--' AND eps_forecast <> '--' THEN
            ROUND(CAST(eps_actual AS NUMERIC) - CAST(eps_forecast AS NUMERIC),2)
        ELSE
          NULL
        END
      AS eps_comparison,
      eps_actual,
      eps_forecast,

      CASE
        WHEN rev_actual <> '--' AND rev_forecast <> '--' THEN
            ROUND(CAST(rev_actual AS NUMERIC) - CAST(rev_forecast AS NUMERIC),2)
        ELSE
          NULL
        END
      AS rev_comparison,

      CASE
        WHEN rev_actual = '--' THEN
          NULL
        ELSE
          CAST(rev_actual AS NUMERIC)
        END
      AS rev_actual,

      CASE
        WHEN rev_forecast = '--' THEN
          NULL
        ELSE
          CAST(rev_forecast AS NUMERIC)
        END
      AS rev_forecast,

      CASE
        WHEN  rev_actual_units = rev_forecast_units THEN
          rev_actual_units
        ELSE
          NULL
        END
      AS rev_units,

      market_cap,
      market_time

FROM  earning_calendar
WHERE Date = timeofday()::DATE;