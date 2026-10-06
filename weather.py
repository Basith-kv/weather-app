import requests
from PIL import Image,ImageTk
import tkinter as tk
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city,unit):

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": unit
    }

    try:
        response = requests.get(url,params=params)
    except requests.exceptions.RequestException:
        return "connection_error"
    
    if response.status_code == 200:

        data = response.json()

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        icon = data["weather"][0]["icon"]
        wind_speed = data["wind"]["speed"]
        country = data["sys"]["country"]
        icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"

        return temperature,feels_like,humidity,description,wind_speed,country,icon_url
    
    else:
        return None
window = tk.Tk()

window.title("Weather App")
window.geometry("450x700")
window.configure(bg="#1e293b")

title_label = tk.Label(
    window,
    text="🌤️Weather App",
    font=("Aria",22,"bold"),
    bg="#1e293b",
    fg="white"
)
title_label.pack(pady=20)

city_label = tk.Label(window,
                      text="Enter City Name",
                      font=("Arial",14,"bold"),
                      bg="#1e293b",
                      fg="white"
                      )
city_label.pack(pady=10)

city_entry = tk.Entry(window,
                      font=("Arial",12),
                      width=25)
city_entry.insert(0, "Enter City Name")

def clear_placeholder(event):
    if city_entry.get() == "Enter City Name":
        city_entry.delete(0,tk.END)

def add_placeholder(event):
    if city_entry.get() == "":
        city_entry.insert(0,"Enter City Name")

city_entry.bind("<FocusIn>", clear_placeholder)
city_entry.bind("<FocusOut>", add_placeholder)

city_entry.pack(pady=10)

unit = tk.StringVar(value="metric")

unit_label = tk.Label(
    window,
    text="Temperature Unit:",
    font=("Arial",11,"bold"),
    bg="#1e293b",
    fg="white"
)

unit_label.pack(pady=5)

celsius_button = tk.Radiobutton(
    window,
    text="Celsius (°C)",
    variable=unit,
    value="metric",
    bg="#1e293b",
    fg="white",
    selectcolor="#334155"
)

celsius_button.pack()

fahrenheit_button = tk.Radiobutton(
    window,
    text="Fahrenheit (°F)",
    variable=unit,
    value="imperial",
    bg="#1e293b",
    fg="white",
    selectcolor="#334155"
)

fahrenheit_button.pack()

def button_click():
    city = city_entry.get().strip()
    city = city.title()

    if city == "" or city == "Enter City Name":
        result_label.configure(
            text="Please enter a city name!"
        )
        return
    result_label.configure(
        text="Getting Weather..."
    )
    window.update()
    result = get_weather(city,unit.get())

    if result == "connection_error":

        result_label.config(
            text="Internet or API connection error!"
        )
        return

    if result:

        temperature,feels_like,humidity,description,wind_speed,country,icon_url = result

        temperature = round(temperature,1)
        feels_like = round(feels_like, 1)
        wind_speed = round(wind_speed, 1)

        if unit.get() == "metric":
            temp_unit = "°C"
            wind_unit = "m/s"
        else:
            temp_unit = "°F"
            wind_unit = "mph"

        description = description.title()

        icon_response = requests.get(icon_url)
        icon_image = Image.open(BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo

        # icon_data = icon_response.content

        # with open("weather icon.png", "wb") as file:
        #     file.write(icon_data)

        result_label.config(
            text=f"City:{city}\n"
                 f"Country:{country}\n"
                 f"Temperature:{temperature} {temp_unit}\n"
                 f"Feels Like:{feels_like} {temp_unit}\n"
                 f"Humidity:{humidity}%\n"
                 f"Weather:{description}\n"
                 f"Wind Speed:{wind_speed} {wind_unit}"
        )
    else:
        result_label.config(text="City not found")

get_button = tk.Button(window,
                       text="Get Weather",
                       command=button_click,
                       font=("Arial",12,"bold"),
                       width=15,
                       bg="white",
                       padx=10,
                       pady=5
                       )
get_button.pack(pady=10)

window.bind("<Return>",lambda event:button_click())

def clear_data():
    city_entry.delete(0,tk.END)
    result_label.config(text="")
    icon_label.config(image="")
    icon_label.image = None

clear_button = tk.Button(
    window,
    text="Clear",
    command=clear_data,
    font=("Arial",11,"bold"),
    width=15,
    bg="white"
)
clear_button.pack(pady=5)

result_frame = tk.Frame(
                        window,
                        bg="white",
                        padx=30,
                        pady=20
)
result_frame.pack(pady=20)

icon_label = tk.Label(
                      result_frame,
                      bg="white")
icon_label.pack()

result_label = tk.Label(
                         result_frame,
                         text="",
                         font=("Arial",12),
                         justify="left",
                         bg="white",
                         padx=10,
                         pady=10
                         )
result_label.pack()

window.mainloop()
