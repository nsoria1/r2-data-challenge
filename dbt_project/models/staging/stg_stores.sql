{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('raw', 'raw_stores') }}
),

validated as (
    select
        store_group,
        store_token,
        store_name,
        _batch_date,
        _loaded_at,
        _source_file,
        
        case
            when store_name is null or trim(store_name) = '' then false
            when length(store_name) >= 200 then false
            else true
        end as is_valid
        
    from source
)

select * from validated
