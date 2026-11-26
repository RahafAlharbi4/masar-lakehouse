with classified as (
    select
        case
            when status is null or status <> 'completed'
                then 'not_completed'
            when ended_at > started_at
                then 'kept'
            else 'invalid_time'
        end as bucket
    from {{ ref('stg_trips') }}
)

select
    count(*) as total,
    count(case when bucket = 'not_completed' then 1 end) as dropped_status,
    count(case when bucket = 'invalid_time' then 1 end) as dropped_time,
    count(case when bucket = 'kept' then 1 end) as kept
from classified