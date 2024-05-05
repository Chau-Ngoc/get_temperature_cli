import os

import requests
from dotenv import load_dotenv

load_dotenv()

ow_apikey = os.getenv("OPENWEATHER_APIKEY")

url = "http://api.openweathermap.org/geo/1.0/direct"
params = {"q": "London,GB", "appid": ow_apikey}

response = requests.get(url, params=params)
print(response.json())
