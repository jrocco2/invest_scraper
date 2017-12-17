DROP VIEW IF EXISTS ECONOMIC_VIEW;

CREATE VIEW ECONOMIC_VIEW AS
SELECT date::DATE as Date,
      date::TIME as TIME,
      event as Event,
      currency as Currency,
      importance as Importance,

      CASE
        WHEN actual IS NOT NULL AND forecast IS NOT NULL THEN
          ROUND(CAST(actual AS NUMERIC) - CAST(forecast AS NUMERIC),2)
        ELSE
          NULL
        END
      AS Comparison,

      CASE
        WHEN actual IS NOT NULL THEN
          CONCAT(ROUND(CAST(actual AS NUMERIC),2),unit)::VARCHAR
        ELSE
          NULL
        END
      as Actual,

      CASE
        WHEN forecast IS NOT NULL THEN
          CONCAT(ROUND(CAST(forecast AS NUMERIC),2),unit)::VARCHAR
        ELSE
          NULL
        END
      as Forecast,

      CASE
        WHEN previous IS NOT NULL THEN
          CONCAT(ROUND(CAST(previous AS NUMERIC),2),unit)::VARCHAR
        ELSE
          NULL
        END
      as Previous

FROM  economic_calendar;
-- WHERE Date = timeofday()::DATE;