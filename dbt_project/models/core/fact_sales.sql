{{
    config(
        materialized='incremental',
        unique_key=['store_token', 'transaction_id'],
        merge_update_columns=['receipt_token', 'transaction_time', 'amount', 'user_role', '_loaded_at', '_source_file']
    )
}}

with source as (
    select * from {{ ref('stg_sales') }}
    where is_valid = true
    
    {% if is_incremental() %}
    and _loaded_at > (select max(_loaded_at) from {{ this }})
    {% endif %}
),

deduplicated as (
    select
        store_token,
        transaction_id,
        receipt_token,
        transaction_time,
        amount,
        user_role,
        _batch_date,
        _loaded_at,
        _source_file,
        
        row_number() over (
            partition by store_token, transaction_id 
            order by _loaded_at desc
        ) as rn
        
    from source
)

select
    store_token,
    transaction_id,
    receipt_token,
    transaction_time,
    amount,
    user_role,
    _batch_date,
    _loaded_at,
    _source_file
from deduplicated
where rn = 1
