import pytest
import assistant
from unittest.mock import patch, MagicMock

def test_get_weather_no_api_key(monkeypatch):
    monkeypatch.setenv("WEATHER_API_KEY", "")
    result = assistant.get_weather("London")
    assert "No API key found" in result

@patch("assistant.requests.get")
def test_get_weather_success(mock_get, monkeypatch):
    monkeypatch.setenv("WEATHER_API_KEY", "fakekey")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "main": {"temp": 20},
        "weather": [{"description": "clear sky"}]
    }
    mock_get.return_value = mock_resp
    result = assistant.get_weather("London")
    assert "🌤️ Weather in London: 20°C, Clear sky" == result

@patch("assistant.requests.get")
def test_get_weather_failure(mock_get, monkeypatch):
    monkeypatch.setenv("WEATHER_API_KEY", "fakekey")
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_get.return_value = mock_resp
    result = assistant.get_weather("London")
    assert "Could not fetch weather data" in result

@patch("assistant.requests.get")
def test_get_joke_single(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "type": "single",
        "joke": "Why did the chicken cross the road? To get to the other side!"
    }
    mock_get.return_value = mock_resp
    result = assistant.get_joke()
    assert "😂 Joke: Why did the chicken cross the road?" in result

@patch("assistant.requests.get")
def test_get_joke_twopart(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "type": "twopart",
        "setup": "Why did the chicken cross the road?",
        "delivery": "To get to the other side!"
    }
    mock_get.return_value = mock_resp
    result = assistant.get_joke()
    assert "😂 Joke: Why did the chicken cross the road?" in result
    assert "...To get to the other side!" in result

@patch("assistant.requests.get")
def test_get_joke_failure(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 500
    mock_get.return_value = mock_resp
    result = assistant.get_joke()
    assert "Could not fetch a joke" in result

def test_add_task_and_list_tasks():
    assistant.tasks.clear()
    result = assistant.add_task("Buy milk")
    assert "✅ Added: 'Buy milk'" == result
    result = assistant.list_tasks()
    assert "1. Buy milk" in result

def test_list_tasks_empty():
    assistant.tasks.clear()
    result = assistant.list_tasks()
    assert "No tasks yet" in result