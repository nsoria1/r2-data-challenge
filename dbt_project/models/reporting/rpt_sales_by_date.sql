{{
    config(
        materialized='view'
    )
}}

with daily_sales as (
    select
        date(transaction_time) as transaction_date,
        count(distinct store_token) as num_stores,
        sum(amount) as total_sales,
        avg(amount) as avg_sales
    from {{ ref('fact_sales') }}
    group by date(transaction_time)
    order by transaction_date desc
    limit 40
),

with_accumulation as (
    select
        current_date as snapshot_date,
        transaction_date,
        num_stores,
        total_sales,
        avg_sales,
        sum(total_sales) over (
            partition by date_trunc('month', transaction_date)
            order by transaction_date
            rows between unbounded preceding and current row
        ) as month_accumulated_sales
    from daily_sales
),

with_top_store as (
    select
        date(f.transaction_time) as transaction_date,
        f.store_token,
        sum(f.amount) as store_sales,
        row_number() over (
            partition by date(f.transaction_time)
            order by sum(f.amount) desc, f.store_token
        ) as rn
    from {{ ref('fact_sales') }} f
    group by date(f.transaction_time), f.store_token
)

select
    ws.snapshot_date,
    ws.transaction_date,
    ws.num_stores,
    ws.total_sales,
    ws.avg_sales,
    ws.month_accumulated_sales,
    ts.store_token as top_store_token
from with_accumulation ws
left join with_top_store ts
    on ws.transaction_date = ts.transaction_date
    and ts.rn = 1
order by ws.transaction_date desc
