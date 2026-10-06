# 🌤️ Weather App

A simple Python Weather Application that fetches real-time weather information using the OpenWeather API.

## Features

- Search weather by city name
- Display temperature
- Display feels-like temperature
- Display humidity
- Display weather condition
- Display wind speed
- Weather icons
- Celsius and Fahrenheit support
- Enter key support
- Clear button
- Invalid city handling
- API connection error handling
- Secure API key using `.env`

## Technologies Used

- Python
- Tkinter
- Requests
- Pillow
- python-dotenv
- OpenWeather API

## How to Run

1. Install the required packages:

```
pip install requests pillow python-dotenv
 

2. Create a .env file:

```
OPENWEATHER_API_KEY=your_api_key
```

3. Run the application:

```
python weather.py
```

Note

The API key is stored in a .env file and excluded from GitHub using .gitignore.

Project Structure

Weather-app
│
├── weather.py
├── README.md
├── .env
└── .gitignore

```