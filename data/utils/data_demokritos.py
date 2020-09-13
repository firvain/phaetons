import json
import pandas as pd

# weather Stations
with open("data\demokritos\\raw\weather_station.json") as f:
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
        my_dict[id]["time"] = my_dict[id]["time"].dt.tz_convert("Europe/Athens")
        my_dict[id]["time"] = my_dict[id]["time"].dt.round("1min")
        my_dict[id]["time"] = pd.to_datetime(my_dict[id]["time"])
        my_dict[id].set_index("time", inplace=True)
        my_dict[id].to_csv(
            "data\demokritos\\refined\weather_station_" + id + ".csv"
        )
        my_dict[id] = my_dict[id].resample("1H").sum()
        my_dict[id].to_csv(
            "data\demokritos\\resampled\weather_station_" + id + ".csv"
        )

# HM_LHLM06 Controller
with open("data\demokritos\\raw\HM_LHLM06.json") as f:
    data = json.load(f)
    columns = data["results"][0]["series"][0]["columns"]
    values = data["results"][0]["series"][0]["values"]
    df = pd.DataFrame(values, columns=columns)

    dfs = dict(tuple(df.groupby("id")))
    my_dict = {}
    for id in df.id.unique():
        my_dict[id] = dfs[id]
        my_dict[id]["time"] = pd.to_datetime(my_dict[id]["time"], utc=True)
        my_dict[id]["time"] = my_dict[id]["time"].dt.tz_convert("Europe/Athens")
        my_dict[id]["time"] = my_dict[id]["time"].dt.round("1min")
        my_dict[id]["time"] = pd.to_datetime(my_dict[id]["time"])
        my_dict[id].set_index("time", inplace=True)
        my_dict[id].to_csv("data\demokritos\\refined\HM_LHLM06_" + id + ".csv")
        my_dict[id] = my_dict[id].resample("1H").sum()
        my_dict[id].to_csv(
            "data\demokritos\\resampled\HM_LHLM06_" + id + ".csv"
        )

# LHLM06 Controller
with open("data\demokritos\\raw\LHLM06.json") as f:
    data = json.load(f)
    columns = data["results"][0]["series"][0]["columns"]
    values = data["results"][0]["series"][0]["values"]
    df = pd.DataFrame(values, columns=columns)

    dfs = dict(tuple(df.groupby("id")))
    my_dict = {}
    for id in df.id.unique():
        my_dict[id] = dfs[id]
        my_dict[id]["time"] = pd.to_datetime(my_dict[id]["time"], utc=True)
        my_dict[id]["time"] = my_dict[id]["time"].dt.tz_convert("Europe/Athens")
        my_dict[id]["time"] = my_dict[id]["time"].dt.round("1min")
        my_dict[id]["time"] = pd.to_datetime(my_dict[id]["time"])
        my_dict[id].set_index("time", inplace=True)
        my_dict[id].to_csv("data\demokritos\\refined\LHLM06_" + id + ".csv")
        my_dict[id] = my_dict[id].resample("1H").sum()
        my_dict[id].to_csv("data\demokritos\\resampled\LHLM06_" + id + ".csv")
