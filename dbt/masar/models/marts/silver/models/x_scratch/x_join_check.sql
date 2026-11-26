with eligible_trips as (
    select driver_id
    from {{ ref('stg_trips') }}
    where status = 'completed'
      and ended_at > started_at
),

drivers as (
    select driver_id
    from {{ ref('stg_drivers') }}
)

select
    (select count(*) from {{ ref('silver_trips') }}) as silver_rows,
    (
        select count(*)
        from eligible_trips t
        inner join drivers d on t.driver_id = d.driver_id
    ) as inner_join_rows,
    (
        select count(*)
        from eligible_trips t
        left anti join drivers d on t.driver_id = d.driver_id
    ) as trips_without_driver