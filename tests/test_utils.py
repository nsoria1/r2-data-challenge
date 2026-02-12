"""Unit tests for src/utils.py"""

import pytest
import tempfile
import os
from src.utils import detect_header, extract_batch_date, get_file_type


def test_detect_header_with_header():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write('store_token,store_name,city\n')
        f.write('ST001,Test Store,New York\n')
        temp_path = f.name
    
    try:
        assert detect_header(temp_path) == True
    finally:
        os.unlink(temp_path)


def test_detect_header_without_header():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write('ST001,Test Store,New York\n')
        f.write('ST002,Another Store,Boston\n')
        temp_path = f.name
    
    try:
        assert detect_header(temp_path) == False
    finally:
        os.unlink(temp_path)


def test_extract_batch_date_valid():
    assert extract_batch_date('stores_20240115.csv') == '20240115'
    assert extract_batch_date('sales_20231225.csv') == '20231225'


def test_extract_batch_date_invalid():
    assert extract_batch_date('stores.csv') is None
    assert extract_batch_date('invalid_file.txt') is None


def test_get_file_type_stores():
    assert get_file_type('stores_20240115.csv') == 'stores'
    assert get_file_type('STORES_20240115.csv') == 'stores'


def test_get_file_type_sales():
    assert get_file_type('sales_20240115.csv') == 'sales'
    assert get_file_type('SALES_20240115.csv') == 'sales'


def test_get_file_type_unknown():
    assert get_file_type('unknown_20240115.csv') is None
    assert get_file_type('data.csv') is None
