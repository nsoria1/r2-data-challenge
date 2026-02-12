{{
    config(
        materialized='view'
    )
}}

with daily_store_sales as (
    select
        date(transaction_time) as transaction_date,
        store_token,
        sum(amount) as store_total_sales
    from {{ ref('fact_sales') }}
    group by date(transaction_time), store_token
),

ranked_stores as (
    select
        transaction_date,
        store_token,
        store_total_sales,
        row_number() over (
            partition by transaction_date
            order by store_total_sales desc, store_token
        ) as rank
    from daily_store_sales
),

latest_dates as (
    select distinct transaction_date
    from ranked_stores
    order by transaction_date desc
    limit 10
)

select
    current_date as snapshot_date,
    rs.transaction_date,
    rs.rank,
    rs.store_total_sales,
    rs.store_token,
    ds.store_name
from ranked_stores rs
join latest_dates ld on rs.transaction_date = ld.transaction_date
join {{ ref('dim_stores') }} ds on rs.store_token = ds.store_token
where rs.rank <= 5
order by rs.transaction_date desc, rs.rank
