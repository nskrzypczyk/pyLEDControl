from dataclasses import dataclass
import datetime
import statistics
import requests
import os
from typing import Dict, List, TypedDict

from misc.logging import Log
from misc.utils import chunk_list
import settings

log = Log("WeatherBinding")


class WeatherForecast(TypedDict):
    time: List[datetime.datetime]
    temperature_2m_avg: List[int]  # in
    temperature_2m_min: List[int]  # in
    temperature_2m_max: List[int]  # in
    rain: List[float]  # in mm
    showers: List[float]  # in mm
    snowfall: List[float]  # in cm
    cloudcover_avg: List[float]  # in %
    cloudcover_min: List[float]  # in %
    cloudcover_max: List[float]  # in %
    precipitation_probability: List[int]  # in %
    icons: List[str]


def is_weather_up_to_date(fc: WeatherForecast) -> bool:
    return fc["time"][0].date() == datetime.date.today()


def _get_all_weather_icons() -> dict:
    png_files = {}

    directory = "display/weather-icons"
    for fn in os.listdir(directory):
        if fn.endswith(".png"):
            file_path = os.path.join(directory, fn)
            file_name = os.path.splitext(fn)[0]
            png_files[file_name] = file_path
    return png_files


def _prepare_output(fc: WeatherForecast) -> WeatherForecast:
    icons = _get_all_weather_icons()
    fc: WeatherForecast
    for i in range(4):
        if fc["precipitation_probability"][i] < 33.3:  # If precip. prob low
            if fc["cloudcover_avg"][i] <= 33:  # if cloudcover is low
                fc["icons"].append(icons["sunny"])
            elif 66 > fc["cloudcover_avg"][i]:
                fc["icons"].append(icons["cloudy"])
            else:
                fc["icons"].append(icons["covered"])
        elif fc["precipitation_probability"][i] > 60 and fc["showers"][i] > 1:
            fc["icons"].append(icons["shower"])
        else:  # if precip. prob high
            if fc["snowfall"][i] >= 1:
                fc["icons"].append(icons["snow"])
            else:
                fc["icons"].append(icons["rain"])
    return fc


class WeatherBinding:
    def __init__(self):
        self.lat: float = settings.WEATHER_LAT
        self.long: float = settings.WEATHER_LONG

    def get(self) -> WeatherForecast:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.long}&hourly=temperature_2m,precipitation_probability,rain,showers,snowfall,cloudcover&timeformat=unixtime&timezone=auto"

        response = requests.get(url)
        data: dict = response.json()["hourly"]

        forecast: WeatherForecast = {k: []
                                     for k in WeatherForecast.__annotations__.keys()}
        li: list
        for k, li in data.items():
            chunked = chunk_list(li, 24)
            if k == "time":
                [forecast[k].append(datetime.datetime.fromtimestamp(ch[0]))
                 for ch in chunked]
            elif k in ["temperature_2m", "cloudcover"]:
                [forecast[k+"_avg"].append(statistics.mean(ch))
                 for ch in chunked]
                [forecast[k+"_min"].append(min(ch)) for ch in chunked]
                [forecast[k+"_max"].append(max(ch)) for ch in chunked]
            else:
                [forecast[k].append(statistics.mean(ch)) for ch in chunked]
        return _prepare_output(forecast)
