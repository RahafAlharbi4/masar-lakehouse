# Masar Capstone Submission

Name: Rahaf Alharbi
Branch: main
Link: https://github.com/RahafAlharbi4/masar-lakehouse/tree/main

## What I built

1. Bronze: Loaded the raw trip, driver, and GPS data into Delta tables.
2. Silver: Built the trips table with dbt. All seven quality checks passed.
3. Delta controls: Rejected a negative fare and added `promo_code` to a demo table.
4. Gold: Built `zone_hourly_demand` by city, date, and hour.
5. BI: Built `bi_trips_safe` with pseudonymized identifiers and coarser location data.
6. Pipeline: Ran all stages with `make pipeline`.
7. Proof: Verified table counts and queried historical Delta versions.

## Counts per layer

- Bronze trips: 48,200
- Bronze drivers: 1,850
- Bronze GPS pings: 120,000
- Silver trips: 44,371
- Gold hourly demand: 120
- BI-safe trips: 44,371

## Time travel

The main Silver table had 44,371 rows in both versions 0 and 5.
A separate demo copy had 44,371 rows in version 0 and 44,370 in version 1
after deleting one trip.

## Steps the trainer handed over
None

## One thing I would improve

Print which Bronze tables are missing if a previous load stopped partway.