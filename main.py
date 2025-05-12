import os
os.environ["TK_SCALING"] = "1.0"

import requests
import customtkinter as ctk
from PIL import Image
from config import API_KEY
from customtkinter import CTkImage
import pygame


pygame.mixer.init()

current_screen = "input"

COLOR_PRIMARY = "#FFFFFF"
COLOR_SECONDARY = "#2e4053"
COLOR_ERROR = "#8B0000"
COLOR_FRAME_BG = "#c9b1f1"
COLOR_BUTTON = "#e28838"
COLOR_BUTTON_HOVER = "#be722f"
COLOR_GET_BUTTON = "#4CAF50"
COLOR_GET_BUTTON_HOVER = "#45A049"

def play_sound(path, play_on_enter=True, event=None):
    if event is None or play_on_enter:
        sound = pygame.mixer.Sound(path)
        sound.play()

def play_background_music(path):
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1)

def stop_background_music():
    pygame.mixer.music.stop()


def fetch_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url)

def get_weather_icon_path(weather_main):
    icon_map = {
        "Clear": "clear.png",
        "Clouds": "clouds.png",
        "Rain": "rain.png",
        "Snow": "snow.png",
        "Thunderstorm": "thunderstorm.png",
        "Drizzle": "rain.png",
        "Mist": "fog.png",
        "Fog": "fog.png"
    }
    return f"icons/{icon_map.get(weather_main, 'clear.png')}"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x450")
app.title("WeatherInsight")

frame = ctk.CTkFrame(master=app, fg_color=COLOR_FRAME_BG)
frame.pack(expand=True, fill="both")
frame.grid_rowconfigure(tuple(range(10)), weight=1)
frame.grid_columnconfigure(tuple(range(5)), weight=1)

city_label = ctk.CTkLabel(frame, text="Enter City Name", font=("Arial", 18, "bold"), text_color=COLOR_PRIMARY)
city_label.grid(row=1, column=2, pady=10)

city_entry = ctk.CTkEntry(frame, width=200)
city_entry.grid(row=2, column=2, pady=10)

def clear_input():
    city_entry.delete(0, 'end')

city_result = ctk.CTkLabel(frame, text="", font=("Arial", 18, "bold"), text_color=COLOR_PRIMARY)
temp_result = ctk.CTkLabel(frame, text="", font=("Arial", 16, "bold"), text_color=COLOR_PRIMARY)
feels_like_result = ctk.CTkLabel(frame, text="", font=("Arial", 14), text_color=COLOR_SECONDARY)
humidity_result = ctk.CTkLabel(frame, text="", font=("Arial", 14), text_color=COLOR_SECONDARY)
wind_result = ctk.CTkLabel(frame, text="", font=("Arial", 14), text_color=COLOR_SECONDARY)
description_result = ctk.CTkLabel(frame, text="", font=("Arial", 14), text_color=COLOR_SECONDARY)

icon_label = ctk.CTkLabel(frame, text="")
icon_label.grid(row=1, column=2)
icon_label.grid_remove()

def handle_enter(event=None):
    global current_screen
    if current_screen == "input":
        on_button_click()  

def show_input_screen():
    global current_screen

    for widget in [city_result, temp_result, feels_like_result, humidity_result, wind_result, description_result, back_button, icon_label]:
        widget.grid_remove()

    city_label.grid()
    city_entry.grid()
    get_button.grid(row=3, column=2, pady=20)
    clear_input()
    city_entry.focus_set()

    current_screen = "input"

def on_button_click(event=None):
    global current_screen

    play_sound("music/button.mp3")

    city = city_entry.get().strip()
    response = fetch_weather_data(city)
    data = response.json()

    if response.status_code != 200:
        play_sound("music/error_2.mp3")
        city_result.configure(text=f"❗ Error: {data.get('message', 'Unknown error.')}", text_color=COLOR_ERROR)
        city_result.grid(row=4, column=2, pady=10)
        clear_input()
        current_screen = "input"
        return

    city_name = data['name']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    weather_main = data['weather'][0]['main']
    description = data['weather'][0]['description']

    icon_path = get_weather_icon_path(weather_main)
    icon_image = Image.open(icon_path)
    icon_ctk_image = CTkImage(light_image=icon_image, size=(100, 100))
    icon_label.configure(image=icon_ctk_image)
    icon_label.image = icon_ctk_image
    icon_label.grid()


    city_result.configure(text=f"📍 City: {city_name}", text_color=COLOR_PRIMARY)
    temp_result.configure(text=f"🌡️ Temperature: {temp}°C", text_color=COLOR_PRIMARY)
    feels_like_result.configure(text=f"🌡️ Feels Like: {feels_like}°C", text_color=COLOR_SECONDARY)
    humidity_result.configure(text=f"💧 Humidity: {humidity}%", text_color=COLOR_SECONDARY)
    wind_result.configure(text=f"💨 Wind Speed: {wind_speed} km/h", text_color=COLOR_SECONDARY)
    description_result.configure(text=f"🌥️ Weather: {description}", text_color=COLOR_SECONDARY)


    for idx, widget in enumerate([city_result, temp_result, feels_like_result, humidity_result, wind_result, description_result], start=3):
        widget.grid(row=idx, column=2, pady=5)

    back_button.grid(row=9, column=2, pady=20)

    city_label.grid_remove()
    city_entry.grid_remove()
    get_button.grid_remove()


    current_screen = "result"

back_button = ctk.CTkButton(
    frame, text="Check Another City",
    command=lambda: [play_sound("music/button.mp3"), show_input_screen()],
    fg_color=COLOR_BUTTON,
    hover_color=COLOR_BUTTON_HOVER,
    text_color="white",
    corner_radius=12,
    font=("Arial", 16, "bold"),
    width=150,
    height=35
)
back_button.grid(row=4, column=2, pady=20)
back_button.grid_remove()

get_button = ctk.CTkButton(
    frame, text="Get Weather",
    command=on_button_click,
    fg_color=COLOR_GET_BUTTON,
    hover_color=COLOR_GET_BUTTON_HOVER,
    text_color="white",
    corner_radius=12,
    font=("Arial", 16, "bold"),
    width=150,
    height=35
)
get_button.grid(row=3, column=2, pady=20)

city_entry.bind("<Return>", handle_enter)

play_background_music("music/lofi_bg.mp3")

app.mainloop()