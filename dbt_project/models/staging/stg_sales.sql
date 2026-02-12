{{
    config(
        materialized='view'
    )
}}

select
    store_token,
    transaction_id,
    receipt_token,
    user_role,
    _batch_date,
    _loaded_at,
    _source_file,
    
    coalesce(
        try_to_timestamp(transaction_time, 'YYYYMMDD"T"HH24MISS.FF3'),
        try_to_timestamp(transaction_time)
    ) as transaction_time,
    
    try_to_decimal(replace(replace(amount, '$', ''), ',', ''), 15, 2) as amount,
    
    case 
        when try_to_timestamp(transaction_time, 'YYYYMMDD"T"HH24MISS.FF3') is null 
             and try_to_timestamp(transaction_time) is null then false
        when try_to_decimal(replace(replace(amount, '$', ''), ',', ''), 15, 2) is null then false
        else true 
    end as is_valid

from {{ source('raw', 'raw_sales') }}
