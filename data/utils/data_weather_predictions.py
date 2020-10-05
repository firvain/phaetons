import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
BASE_DATA_DIR = os.getenv("BASE_DATA_DIR")
openweathermap_api_key =  os.getenv("OPENWEATHER_API_KEY")

locations = {
    "Athens": {"lat": 37.97945, "lon": 23.716221},
    "Alistrati": {"lat": 41.069313, "lon": 23.9536466},
    "Agiou_Dimitriou": {"lat": 40.6403, "lon": 22.9439},
}


def get_openweather_data(lat, lon, location):
    """
    docstring
    """
    payload = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely,daily,current",
        "units": "metric",
        "appid": "92b69cab756190235357327d2cab3e25",
    }
    url = "https://api.openweathermap.org/data/2.5/onecall"
    try:
        r = requests.get(url, params=payload)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    j = r.json()
    df = pd.DataFrame.from_dict(j["hourly"])
    df.drop(["feels_like", "weather", "pop"], axis=1, inplace=True)
    df["dt"] = pd.to_datetime(df["dt"], unit="s", utc=True).dt.tz_convert(
        "Europe/Athens"
    )
    df.rename(columns={"dt": "time", "temp": "temperature"}, inplace=True)
    df.set_index("time", inplace=True)
    file_name = df.iloc[0].name.strftime("%Y_%m_%d") + "_" + location + ".csv"
    p = Path(BASE_DATA_DIR + "/openweathermap")
    df.to_csv(p / file_name)


def main():
    for location in locations:
        coords = locations.get(location)
        get_openweather_data(coords["lat"], coords["lon"], location)


if __name__ == "__main__":
    main()
