import tkinter as tk
from tkinter import font
import requests

API_KEY = "2f02b82dfad491647bc9ab02132cd3db"

def get_weather():
    city = city_entry.get().strip()
    if not city:
        result_label.config(text="Please enter a city name", fg="#e74c3c")
        return
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ar"
        response = requests.get(url, timeout=10)
        data = response.json()
        if response.status_code == 200:
            temp = data["main"]["temp"]
            feels = data["main"]["feels_like"]
            weather = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            country = data["sys"]["country"]
            result_label.config(fg="#2c3e50", text=f"📍 {city.title()}, {country}\n\n🌡  Temperature : {temp}°C  (feels like {feels}°C)\n🌤  Weather     : {weather}\n💧 Humidity    : {humidity}%\n💨 Wind Speed  : {wind} m/s")
        elif response.status_code == 401:
            result_label.config(fg="#e74c3c", text="Invalid API Key or not activated yet")
        elif response.status_code == 404:
            try:
                geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
                geo_res = requests.get(geo_url, timeout=10).json()
                if geo_res:
                    lat, lon = geo_res[0]["lat"], geo_res[0]["lon"]
                    url2 = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=ar"
                    data2 = requests.get(url2, timeout=10).json()
                    temp = data2["main"]["temp"]
                    feels = data2["main"]["feels_like"]
                    weather = data2["weather"][0]["description"]
                    humidity = data2["main"]["humidity"]
                    wind = data2["wind"]["speed"]
                    country = data2["sys"]["country"]
                    result_label.config(fg="#2c3e50", text=f"📍 {city}, {country}\n\n🌡  Temperature : {temp}°C  (feels like {feels}°C)\n🌤  Weather     : {weather}\n💧 Humidity    : {humidity}%\n💨 Wind Speed  : {wind} m/s")
                else:
                    result_label.config(fg="#e74c3c", text=f"City '{city}' not found")
            except:
                result_label.config(fg="#e74c3c", text=f"City '{city}' not found")
        else:
            result_label.config(fg="#e74c3c", text=f"Error {response.status_code}: {data.get('message', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        result_label.config(fg="#e74c3c", text="No internet connection")
    except requests.exceptions.Timeout:
        result_label.config(fg="#e74c3c", text="Request timed out, try again")
    except Exception as e:
        result_label.config(fg="#e74c3c", text=f"Unexpected error: {e}")

root = tk.Tk()
root.title("Weather App")
root.geometry("380x300")
root.configure(bg="#ecf0f1")
root.resizable(False, False)
title_font = font.Font(family="Helvetica", size=16, weight="bold")
label_font = font.Font(family="Helvetica", size=11)
result_font = font.Font(family="Courier", size=10)
tk.Label(root, text="🌦 Weather App", font=title_font, bg="#ecf0f1", fg="#2c3e50").pack(pady=(15, 5))
tk.Label(root, text="Enter City Name:", font=label_font, bg="#ecf0f1", fg="#555").pack()
city_entry = tk.Entry(root, font=label_font, width=25, relief="flat", bd=2, bg="white")
city_entry.pack(pady=6, ipady=4)
city_entry.focus()
city_entry.bind("<Return>", lambda e: get_weather())
tk.Button(root, text="Get Weather", command=get_weather, font=label_font, bg="#3498db", fg="white", relief="flat", padx=12, pady=4, cursor="hand2").pack(pady=6)
result_label = tk.Label(root, text="", font=result_font, bg="#ecf0f1", fg="#2c3e50", justify="left")
result_label.pack(pady=10)
root.mainloop()