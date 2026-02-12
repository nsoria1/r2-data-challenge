{{
    config(
        materialized='incremental',
        unique_key='store_token',
        merge_update_columns=['store_group', 'store_name', '_loaded_at', '_source_file']
    )
}}

with source as (
    select * from {{ ref('stg_stores') }}
    where is_valid = true
    
    {% if is_incremental() %}
    and _loaded_at > (select max(_loaded_at) from {{ this }})
    {% endif %}
),

deduplicated as (
    select
        store_group,
        store_token,
        store_name,
        _batch_date,
        _loaded_at,
        _source_file,
        
        row_number() over (
            partition by store_token 
            order by _loaded_at desc
        ) as rn
        
    from source
)

select
    store_group,
    store_token,
    store_name,
    _batch_date,
    _loaded_at,
    _source_file
from deduplicated
where rn = 1
