import os
from typing import Tuple

import click
import requests
from dotenv import load_dotenv

load_dotenv()

ow_apikey = os.getenv("OPENWEATHER_APIKEY")


def get_coords_from_location_name(
    location_name: str, apikey: str
) -> Tuple[float, float]:
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": location_name, "appid": apikey}

    response = requests.get(url, params=params)
    response_json = response.json()
    lat, lon = response_json[0]["lat"], response_json[0]["lon"]

    return lat, lon


def get_temperature_from_lat_lon(
    lat: float, lon: float, apikey: str, units: str
) -> float:
    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": apikey,
        "exclude": "minutely,hourly,daily,alerts",
        "units": units,
    }

    response = requests.get(url, params=params)
    response_json = response.json()

    return response_json["current"]["temp"]


@click.command()
@click.argument("location")
@click.option(
    "--units",
    default="metric",
    type=click.Choice(["standard", "metric", "imperial"], case_sensitive=False),
)
def get_temperature(location, units):
    lat, lon = get_coords_from_location_name(location, ow_apikey)
    temperature = get_temperature_from_lat_lon(lat, lon, ow_apikey, units=units)
    click.echo(temperature)
