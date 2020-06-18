from pandas import read_csv
from datetime import datetime
import numpy as np


# load data
def parse(x):
    return datetime.strptime(x, "%Y %m %d %H")


dataset = read_csv(
    "data/raw.csv",
    parse_dates=[["year", "month", "day", "hour"]],
    index_col=0,
    date_parser=parse,
)
dataset.drop(
    ["No", "pm2.5", "DEWP", "TEMP", "PRES", "Is", "Ir"], axis=1, inplace=True
)
# manually specify column names
dataset.columns = [
    "wnd_dir",
    "wnd_spd",
]
dataset.index.name = "date"
cols = list(dataset.columns.values)
# cols.pop(cols.index("wnd_dir"))
dataset = dataset[cols]
dataset["PW"] = np.random.uniform(0, 100, len(dataset))
# mark all NA values with 0
# dataset["pollution"].fillna(0, inplace=True)
# drop the first 24 hours
dataset = dataset[24:]
# summarize first 5 rows
print(dataset.head(5))
# save to file
dataset.to_csv("data/WindTurbine.csv")
