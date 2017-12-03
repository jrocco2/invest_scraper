CREATE VIEW ECONOMIC_VIEW AS
SELECT date::DATE as Date,
      date::TIME as TIME,
      event as Event,
      currency as Currency,
      importance as Importance,

      CASE
        WHEN actual <> '' AND forecast <> '' THEN
            ROUND(CAST(actual AS NUMERIC) - CAST(forecast AS NUMERIC),2)
        ELSE
          NULL
        END
      AS Comparison,

      CASE
        WHEN actual <> '' THEN
          CONCAT(actual,actual_unit)
        ELSE
          NULL
        END
      as Actual,

      CASE
        WHEN forecast <> '' THEN
          CONCAT(forecast,forecast_unit)
        ELSE
          NULL
        END
      as Forecast,

      CASE
        WHEN previous <> '' THEN
          CONCAT(previous,previous_unit)
        ELSE
          NULL
        END
      as Previous

FROM  economic_calendar;
WHERE Date = timeofday()::DATE;