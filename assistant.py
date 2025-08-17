import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# --- Persistent Task Storage ---
TASKS_FILE = "tasks.json"


# --- Core Functions ---
def get_weather(city):
    """Fetch weather data from OpenWeatherMap API."""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "⚠️ Error: No API key found. Get one from https://openweathermap.org/"
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"🌤️ Weather in {city}: {temp}°C, {desc.capitalize()}"
    else:
        return "⚠️ Error: Could not fetch weather data."

def get_joke():
    """Fetch a random joke from the JokeAPI."""
    url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data["type"] == "single":
            return f"😂 Joke: {data['joke']}"
        else:
            return f"😂 Joke: {data['setup']}\n...{data['delivery']}"
    else:
        return "⚠️ Error: Could not fetch a joke."

# --- Task Manager ---
tasks = []

def add_task(task):
    tasks.append(task)
    return f"✅ Added: '{task}'"

def list_tasks():
    if not tasks:
        return "📝 No tasks yet!"
    return "📝 Your Tasks:\n" + "\n".join(f"{i+1}. {task}" for i, task in enumerate(tasks))

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)

# Initialize tasks
tasks = load_tasks()

# --- Enhanced Features ---
def get_news(topic="technology"):
    """Fetch top news headlines from NewsAPI"""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return "⚠️ Error: No NewsAPI key found."
    
    url = f"https://newsapi.org/v2/top-headlines?category={topic}&apiKey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        articles = response.json().get("articles", [])[:5]  # Get top 5
        if not articles:
            return "No news found for this topic."
        
        news_output = ["📰 Top News Headlines:"]
        for i, article in enumerate(articles, 1):
            news_output.append(f"{i}. {article['title']} ({article['source']['name']})")
        return "\n".join(news_output)
    else:
        return "⚠️ Error: Could not fetch news."

def convert_currency(amount, from_curr, to_curr):
    """Convert currency using ExchangeRate-API"""
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        return "⚠️ Error: No ExchangeRate API key found."
    
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_curr.upper()}/{to_curr.upper()}/{amount}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("result") == "success":
            rate = data["conversion_rate"]
            converted = data["conversion_result"]
            return f"💱 {amount} {from_curr.upper()} = {converted:.2f} {to_curr.upper()} (Rate: {rate:.4f})"
    return "⚠️ Error: Could not convert currency."

# --- Modified Task Functions ---
def add_task(task):
    task_id = len(tasks) + 1
    task_data = {
        "id": task_id,
        "task": task,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "completed": False
    }
    tasks.append(task_data)
    save_tasks(tasks)
    return f"✅ Added Task #{task_id}: '{task}'"

def list_tasks():
    if not tasks:
        return "📝 No tasks yet!"
    
    output = ["📝 Your Tasks:"]
    for task in tasks:
        status = "✓" if task["completed"] else " "
        output.append(f"{task['id']}. [{status}] {task['task']} (Added: {task['created_at']})")
    return "\n".join(output)

def complete_task(task_id):
    try:
        task_id = int(task_id)
        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = True
                save_tasks(tasks)
                return f"🎉 Completed Task #{task_id}: '{task['task']}'"
        return "⚠️ Task not found."
    except ValueError:
        return "⚠️ Please enter a valid task ID."

# --- Updated Main CLI ---
def main():
    print("🌟 PyAssistant v2.0 - Enhanced Edition 🌟")
    print("Commands:")
    print("- weather <city>  : Get weather forecast")
    print("- joke            : Get a random joke")
    print("- news [topic]    : Get top news (default: technology)")
    print("- convert <amount> <from> <to> : Currency conversion")
    print("- add <task>      : Add a new task")
    print("- list            : Show all tasks")
    print("- complete <id>   : Mark task as done")
    print("- exit            : Quit the program")
    
    while True:
        command = input("\n> ").strip().lower()
        
        if command.startswith("weather "):
            city = command.split(" ", 1)[1]
            print(get_weather(city))
        
        elif command == "joke":
            print(get_joke())
        
        elif command.startswith("news"):
            topic = command.split(" ", 1)[1] if " " in command else "technology"
            print(get_news(topic))
        
        elif command.startswith("convert "):
            try:
                _, amount, from_curr, to_curr = command.split()
                print(convert_currency(float(amount), from_curr, to_curr))
            except:
                print("⚠️ Usage: convert <amount> <from_currency> <to_currency>")
        
        elif command.startswith("add "):
            task = command.split(" ", 1)[1]
            print(add_task(task))
        
        elif command == "list":
            print(list_tasks())
        
        elif command.startswith("complete "):
            task_id = command.split(" ", 1)[1]
            print(complete_task(task_id))
        
        elif command == "exit":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Unknown command. Type 'help' for options.")

if __name__ == "__main__":
    main()