{{
    config(
        materialized='view'
    )
}}

select
    current_date as snapshot_date,
    _batch_date as batch_date,
    count(*) as total_raw_transactions,
    sum(case when is_valid then 1 else 0 end) as valid_transactions,
    sum(case when not is_valid then 1 else 0 end) as invalid_transactions,
    max(date(_loaded_at)) as processing_date
from {{ ref('stg_sales') }}
group by _batch_date
order by _batch_date desc
limit 40
