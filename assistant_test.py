import pytest
import assistant
from unittest.mock import patch, MagicMock
from datetime import datetime

def setup_module(module):
    # Backup and clear tasks file before tests
    try:
        with open(assistant.TASKS_FILE, "r") as f:
            module._backup = f.read()
    except FileNotFoundError:
        module._backup = None
    with open(assistant.TASKS_FILE, "w") as f:
        f.write("[]")
    assistant.tasks.clear()

def teardown_module(module):
    # Restore tasks file after tests
    if module._backup is not None:
        with open(assistant.TASKS_FILE, "w") as f:
            f.write(module._backup)
    else:
        try:
            os.remove(assistant.TASKS_FILE)
        except FileNotFoundError:
            pass

@patch("assistant.requests.get")
def test_get_news_no_api_key(mock_get, monkeypatch):
    monkeypatch.setenv("NEWS_API_KEY", "")
    result = assistant.get_news("technology")
    assert "No NewsAPI key found" in result

@patch("assistant.requests.get")
def test_get_news_success(mock_get, monkeypatch):
    monkeypatch.setenv("NEWS_API_KEY", "fakekey")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "articles": [
            {"title": "Title1", "source": {"name": "Source1"}},
            {"title": "Title2", "source": {"name": "Source2"}},
        ]
    }
    mock_get.return_value = mock_resp
    result = assistant.get_news("technology")
    assert "📰 Top News Headlines:" in result
    assert "1. Title1 (Source1)" in result

@patch("assistant.requests.get")
def test_get_news_no_articles(mock_get, monkeypatch):
    monkeypatch.setenv("NEWS_API_KEY", "fakekey")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"articles": []}
    mock_get.return_value = mock_resp
    result = assistant.get_news("technology")
    assert "No news found for this topic." in result

@patch("assistant.requests.get")
def test_get_news_error(mock_get, monkeypatch):
    monkeypatch.setenv("NEWS_API_KEY", "fakekey")
    mock_resp = MagicMock()
    mock_resp.status_code = 500
    mock_get.return_value = mock_resp
    result = assistant.get_news("technology")
    assert "Could not fetch news" in result

@patch("assistant.requests.get")
def test_convert_currency_no_api_key(mock_get, monkeypatch):
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "")
    result = assistant.convert_currency(10, "usd", "eur")
    assert "No ExchangeRate API key found" in result

@patch("assistant.requests.get")
def test_convert_currency_success(mock_get, monkeypatch):
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "fakekey")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "result": "success",
        "conversion_rate": 0.9,
        "conversion_result": 9.0
    }
    mock_get.return_value = mock_resp
    result = assistant.convert_currency(10, "usd", "eur")
    assert "💱 10 USD = 9.00 EUR" in result

@patch("assistant.requests.get")
def test_convert_currency_failure(mock_get, monkeypatch):
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "fakekey")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"result": "error"}
    mock_get.return_value = mock_resp
    result = assistant.convert_currency(10, "usd", "eur")
    assert "Could not convert currency" in result

def test_add_task_and_list_tasks():
    assistant.tasks.clear()
    with patch("assistant.save_tasks") as mock_save:
        result = assistant.add_task("Buy milk")
        assert "✅ Added Task #1: 'Buy milk'" == result
        assert len(assistant.tasks) == 1
        assert assistant.tasks[0]["task"] == "Buy milk"
        mock_save.assert_called_once()
    result = assistant.list_tasks()
    assert "1. [ ] Buy milk" in result

def test_list_tasks_empty():
    assistant.tasks.clear()
    result = assistant.list_tasks()
    assert "No tasks yet" in result

def test_complete_task_success():
    assistant.tasks.clear()
    with patch("assistant.save_tasks") as mock_save:
        assistant.add_task("Buy eggs")
        result = assistant.complete_task(1)
        assert "🎉 Completed Task #1: 'Buy eggs'" == result
        assert assistant.tasks[0]["completed"] is True
        mock_save.assert_called_once()

def test_complete_task_not_found():
    assistant.tasks.clear()
    result = assistant.complete_task(99)
    assert "Task not found" in result

def test_complete_task_invalid_id():
    assistant.tasks.clear()
    result = assistant.complete_task("abc")
    assert "Please enter a valid task ID" in result