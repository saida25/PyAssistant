import os
import requests
from dotenv import load_dotenv
import json

# Load environment variables (for API keys)
load_dotenv()

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
        print(data)
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

# --- Main CLI ---
def main():
    print("🌟 PyAssistant - Your Personal CLI Helper 🌟")
    print("Commands: weather <city>, joke, add <task>, list, exit")
    
    while True:
        command = input("\n> ").strip().lower()
        
        if command.startswith("weather "):
            city = command.split(" ", 1)[1]
            print(get_weather(city))
        elif command == "joke":
            print(get_joke())
        elif command.startswith("add "):
            task = command.split(" ", 1)[1]
            print(add_task(task))
        elif command == "list":
            print(list_tasks())
        elif command == "exit":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Unknown command. Try: weather <city>, joke, add <task>, list, exit")

if __name__ == "__main__":
    main()