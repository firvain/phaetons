import json
import requests
import pandas as pd
from pathlib import Path
import argparse
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
BASE_DATA_DIR = os.getenv("BASE_DATA_DIR")
raw_path = Path(BASE_DATA_DIR + "/demokritos/raw")
refined_path = Path(BASE_DATA_DIR + "/demokritos/refined")
resampled_path = Path(BASE_DATA_DIR + "/demokritos/resampled")

parser = argparse.ArgumentParser()
parser.add_argument("-t,", "--time", required=False, help="from time")
args = parser.parse_args()


def get_data_from_demokritos(device, d=None):
    """[Get data from Demokritos Server]

    Args:
        device ([str]): [type of device].
            Accepted values "weather_station", "LHLM06", "HM_LHLM06"
        d ([str], optional): [description]. Defaults to None.

    Raises:
        SystemExit: [description]

    Returns:
        [obj]: [json data]
    """
    try:
        print(device)
        if d is not None:
            url = (
                "https://phaetons.dat.demokritos.gr/data/hybrid?device="
                + device
                + "&from="
                + d
            )
        else:
            url = (
                "https://phaetons.dat.demokritos.gr/data/hybrid?device="
                + device
            )
        r = requests.get(url, headers={"devkey": "UzShuDf3vmxi95lksG4k"})
        r.raise_for_status()
        data = r.json()
        return data
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def save_data_to_json(device, data):
    """Save Demoritos data to json

    Args:
        name ([str]): base file name
    """
    file_name = datetime.now().strftime("%Y_%m_%d") + "_" + device + ".json"
    file_path = raw_path / file_name
    with open(file_path, "w") as f:
        json.dump(data, f)


def refine_weather_station(device):
    file_name = datetime.now().strftime("%Y_%m_%d") + "_" + device + ".json"

    with open(raw_path / file_name) as f:
        data = json.load(f)
        columns = data["results"][0]["series"][0]["columns"]
        values = data["results"][0]["series"][0]["values"]
        df = pd.DataFrame(values, columns=columns)
        df = df.drop(["packets"], axis=1)

        dfs = dict(tuple(df.groupby("id")))
        my_dict = {}
        for id in df.id.unique():
            my_dict[id] = dfs[id]
            my_dict[id]["time"] = pd.to_datetime(my_dict[id]["time"], utc=True)
            my_dict[id]["time"] = my_dict[id]["time"].dt.tz_convert(
                "Europe/Athens"
            )
            my_dict[id]["time"] = my_dict[id]["time"].dt.round("1min")
            my_dict[id]["time"] = pd.to_datetime(my_dict[id]["time"])
            my_dict[id].set_index("time", inplace=True)
            refined_file = (
                datetime.now().strftime("%Y_%m_%d")
                + " "
                + device
                + "_"
                + id
                + ".csv"
            )
            my_dict[id].to_csv(refined_path / refined_file)
            my_dict[id] = my_dict[id].resample("1H").mean()
            resampled_file = (
                datetime.now().strftime("%Y_%m_%d")
                + " "
                + device
                + " "
                + id
                + ".csv"
            )
            my_dict[id].to_csv(resampled_path / resampled_file)
            base_file = "weather_station" + "_" + id + ".csv"
            my_dict[id].to_csv(
                resampled_path / base_file,
                mode="a",
                header=not (resampled_path / base_file).exists(),
            )


# HM_LHLM06 Controller
def refine_HM_LHLM06(device):
    file_name = datetime.now().strftime("%Y_%m_%d") + "_" + device + ".json"

    with open(raw_path / file_name) as f:
        data = json.load(f)
        columns = data["results"][0]["series"][0]["columns"]
        values = data["results"][0]["series"][0]["values"]
        df = pd.DataFrame(values, columns=columns)

        dfs = dict(tuple(df.groupby("id")))
        my_dict = {}
        for id in df.id.unique():
            my_dict[id] = dfs[id]
            my_dict[id]["time"] = pd.to_datetime(my_dict[id]["time"], utc=True)
            my_dict[id]["time"] = my_dict[id]["time"].dt.tz_convert(
                "Europe/Athens"
            )
            my_dict[id]["time"] = my_dict[id]["time"].dt.round("1min")
            my_dict[id]["time"] = pd.to_datetime(my_dict[id]["time"])
            my_dict[id].set_index("time", inplace=True)
            refined_file = (
                datetime.now().strftime("%Y_%m_%d")
                + " "
                + device
                + "_"
                + id
                + ".csv"
            )
            my_dict[id].to_csv(refined_path / refined_file)
            my_dict[id] = my_dict[id].resample("1H").mean()
            resampled_file = (
                datetime.now().strftime("%Y_%m_%d")
                + " "
                + device
                + " "
                + id
                + ".csv"
            )
            my_dict[id].to_csv(resampled_path / resampled_file)
            base_file = "HM_LHLM06" + "_" + id + ".csv"
            my_dict[id].to_csv(
                resampled_path / base_file,
                mode="a",
                header=not (resampled_path / base_file).exists(),
            )


# LHLM06 Controller
def refine_LHLM06(device):
    file_name = datetime.now().strftime("%Y_%m_%d") + "_" + device + ".json"

    with open(raw_path / file_name) as f:
        data = json.load(f)
        columns = data["results"][0]["series"][0]["columns"]
        values = data["results"][0]["series"][0]["values"]
        df = pd.DataFrame(values, columns=columns)

        dfs = dict(tuple(df.groupby("id")))
        my_dict = {}
        for id in df.id.unique():
            my_dict[id] = dfs[id]
            my_dict[id]["time"] = pd.to_datetime(my_dict[id]["time"], utc=True)
            my_dict[id]["time"] = my_dict[id]["time"].dt.tz_convert(
                "Europe/Athens"
            )
            my_dict[id]["time"] = my_dict[id]["time"].dt.round("1min")
            my_dict[id]["time"] = pd.to_datetime(my_dict[id]["time"])
            my_dict[id].set_index("time", inplace=True)
            refined_file = (
                datetime.now().strftime("%Y_%m_%d")
                + " "
                + device
                + "_"
                + id
                + ".csv"
            )
            my_dict[id].to_csv(refined_path / refined_file)
            my_dict[id] = my_dict[id].resample("1H").mean()
            resampled_file = (
                datetime.now().strftime("%Y_%m_%d")
                + " "
                + device
                + " "
                + id
                + ".csv"
            )
            my_dict[id].to_csv(resampled_path / resampled_file)
            base_file = "LHLM06" + "_" + id + ".csv"
            my_dict[id].to_csv(
                resampled_path / base_file,
                mode="a",
                header=not (resampled_path / base_file).exists(),
            )


def main():
    devices = ["weather_station", "LHLM06", "HM_LHLM06"]
    for device in devices:
        data = get_data_from_demokritos(device, args.time)
        save_data_to_json(device, data)

    refine_weather_station("weather_station")
    refine_LHLM06("LHLM06")
    refine_HM_LHLM06("HM_LHLM06")


if __name__ == "__main__":
    main()
