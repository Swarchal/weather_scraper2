import os
from collections import namedtuple

import requests
import config


def get_weather(city="London", apikey=None):
    """get JSON response from openweathermap"""
    if apikey is None:
        try:
            api_key = config.API_KEY
        except KeyError:
            raise Exception("No API key found")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception()


def format_response(response_json):
    """format response into a named tuple"""
    record = {
        "lon": response_json["coord"]["lon"],
        "lat": response_json["coord"]["lat"],
        "weather_description": response_json["weather"][0]["description"],
        "temp": response_json["main"]["temp"],
        "temp_feels_like": response_json["main"]["feels_like"],
        "temp_min": response_json["main"]["temp_min"],
        "temp_max": response_json["main"]["temp_max"],
        "pressure": response_json["main"]["pressure"],
        "humidity": response_json["main"]["humidity"],
        "visibility": response_json["visibility"],
        "wind_speed": response_json["wind"]["speed"],
        "wind_deg": response_json["wind"]["deg"],
        "datetime": response_json["dt"],
        "timezone": response_json["timezone"],
        "city_name": response_json["name"],
        "city_id": response_json["id"],
        "sunrise": response_json["sys"]["sunrise"],
        "sunset": response_json["sys"]["sunset"],
    }
    return record
