{{ config(materialized='view') }}

select *
from {{ ref('silver_trips') }}