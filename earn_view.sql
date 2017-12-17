DROP VIEW IF EXISTS EARNING_VIEW;

CREATE VIEW EARNING_VIEW AS
SELECT date::DATE as Date,
      date::TIME as TIME,
      country,
      company,
      short_code as CODE,

      CASE
        WHEN eps_actual IS NOT NULL AND eps_forecast IS NOT NULL THEN
          ROUND(CAST(eps_actual AS NUMERIC) - CAST(eps_forecast AS NUMERIC),2)
        ELSE
          NULL
        END
      AS eps_comparison,
      eps_actual,
      eps_forecast,

      CASE
        WHEN rev_actual IS NOT NULL AND rev_forecast IS NOT NULL THEN
            rev_actual - rev_forecast
        ELSE
          NULL
        END
      AS rev_comparison,

      rev_actual,
      rev_forecast,
      market_cap,
      market_time

FROM  earning_calendar;
--WHERE Date = timeofday()::DATE;