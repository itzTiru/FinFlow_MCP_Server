import pytest
import json
from src.stock_data import get_stock_data_by_period, get_stock_data_by_dates

def test_get_stock_data_by_period_valid():
    result = get_stock_data_by_period("AAPL", "1d")
    assert isinstance(result, str)
    try:
        data = json.loads(result)
        assert isinstance(data, list)  # Expect list of records
        assert "error" not in data
    except json.JSONDecodeError:
        pytest.fail("Result is not valid JSON")

def test_get_stock_data_by_period_invalid_ticker():
    result = get_stock_data_by_period("INVALID", "1d")
    data = json.loads(result)
    assert "error" in data
    assert "No data available" in data["error"]

def test_get_stock_data_by_period_invalid_period():
    result = get_stock_data_by_period("AAPL", "invalid")
    data = json.loads(result)
    assert "error" in data
    assert "Invalid time period" in data["error"]

def test_get_stock_data_by_dates_valid():
    result = get_stock_data_by_dates("AAPL", "2025-09-01", "2025-09-15")
    assert isinstance(result, str)
    try:
        data = json.loads(result)
        assert isinstance(data, list)
        assert "error" not in data
    except json.JSONDecodeError:
        pytest.fail("Result is not valid JSON")

def test_get_stock_data_by_dates_invalid_date():
    result = get_stock_data_by_dates("AAPL", "2025-13-01", "2025-09-15")
    data = json.loads(result)
    assert "error" in data
    assert "Invalid date format" in data["error"]