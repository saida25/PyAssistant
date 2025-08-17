# PyAssistant 🤖

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A customizable personal assistant CLI tool built with Python that helps with daily tasks, information fetching, and productivity.

![PyAssistant Demo GIF](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDk0cGZ0b2F4b3FmY2x1dWJ6cXZ4Z2VlY2J6eGZxZ3B2eWZ1eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/example.gif) 
*(Replace with actual demo GIF)*

## ✨ Features

- **Task Management** 📝
  - Add, list, and complete tasks
  - Persistent storage using JSON
  - Timestamp tracking

- **Information Tools** ℹ️
  - Real-time weather lookup (`weather <city>`)
  - Currency conversion (`convert <amount> <from> <to>`)
  - News headlines (`news [topic]`)
  - Random jokes (`joke`)

- **Extensible Architecture** 🔌
  - Easy to add new commands
  - API-based services
  - Modular design

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/saida25/PyAssistant.git
cd pyassistant
```

2. Set up environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure API keys:
```bash
cp .env.example .env
```
Edit `.env` with your API keys:
- [OpenWeatherMap](https://openweathermap.org/api)
- [NewsAPI](https://newsapi.org/)
- [ExchangeRate-API](https://www.exchangerate-api.com/)

## 🛠️ Usage

Run the assistant:
```bash
python assistant.py
```

**Available Commands:**
```
weather <city>      Get weather forecast
joke                Get a random joke
news [topic]        Get top news (default: technology)
convert <amt> <from> <to>  Currency conversion
add <task>          Add a new task
list                Show all tasks
complete <id>       Mark task as done
exit                Quit the program
```

## 🌟 Example Session

```bash
> weather Tokyo
🌤️ Weather in Tokyo: 22°C, Scattered clouds

> convert 100 usd eur
💱 100 USD = 93.50 EUR (Rate: 0.9350)

> add Buy milk
✅ Added Task #1: 'Buy milk'

> complete 1
🎉 Completed Task #1: 'Buy milk'
```

## 📂 Project Structure

```
pyassistant/
├── .env                # Environment variables
├── assistant.py        # Main application
├── tasks.json          # Task storage (auto-generated)
├── requirements.txt    # Dependencies
└── README.md           # This file
```

## 🤝 How to Contribute

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact

Saida YENGUI - saida.yengui@gmail.com

Project Link: [https://github.com/saida25/PyAssistant]
