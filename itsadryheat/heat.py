import os

import pandas as pd
import requests
import streamlit as st
from geopy.geocoders import Nominatim

OPENWEATHER_KEY = os.environ.get("OPENWEATHER_API_KEY", "DefaultKey")


def get_coordinates(
    location_name: str = "Perth, Western Australia",
) -> tuple[float | None, float | None]:
    """
    Get the latitude and longitude coordinates of a given location name.

    :param location_name: Name of the location to geocode
    :type location_name: str
    :return: Tuple containing latitude and longitude
    :rtype: Tuple[Optional[float], Optional[float]]
    """

    geolocator = Nominatim(user_agent="dryheat")
    if location := geolocator.geocode(location_name):
        return location.latitude, location.longitude
    else:
        return None, None


# Function to fetch weather data
def fetch_weather_data(OPENWEATHER_KEY, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,daily,alerts&units=metric&appid={OPENWEATHER_KEY}"
    response = requests.get(url)
    return response.json()["hourly"]


st.title("But its a dry heat")
lat, lon = get_coordinates()
data = fetch_weather_data(OPENWEATHER_KEY, lat, lon)

df = pd.DataFrame(data)
df["date"] = pd.to_datetime(df["dt"], unit="s")
df.set_index("date", inplace=True)

# Keep only the last week's data (24*7 hours)
# df = df.tail(24 * 7)

# Plotting
st.line_chart(
    df[["temp", "humidity"]].rename(
        columns={"temp": "Temperature (°C)", "humidity": "Humidity (%)"}
    )
)
