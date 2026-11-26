with trips as (
    select *
    from {{ ref('x_silver_copy') }}
),

repeated_cities as (
    select city
    from trips
    where city is not null
    group by city
    having count(*) > 1
)

select 'unique_city' as test_name, count(*) as n
from repeated_cities

union all

select 'accepted_values_city', count(distinct city)
from trips
where city not in ('Riyadh', 'Jeddah', 'Dammam', 'Mecca')

union all

select 'accepted_range_fare', count(*)
from trips
where fare_sar < 30

union all

select 'not_null_geohash', count(*)
from trips
where dropoff_geohash is null