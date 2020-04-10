from pandas import read_csv
from datetime import datetime


# load data
def parse(x):
    return datetime.strptime(x, "%Y %m %d %H")


dataset = read_csv(
    "data/pollution.txt",
    parse_dates=[["year", "month", "day", "hour"]],
    index_col=0,
    date_parser=parse,
)
dataset.drop("No", axis=1, inplace=True)
dataset.drop("cbwd", axis=1, inplace=True)
dataset.drop(dataset.loc[:, "DEWP":"PRES"].columns, axis=1, inplace=True)
dataset.drop(dataset.loc[:, "Is":"Ir"].columns, axis=1, inplace=True)
# manually specify column names
print(dataset.head(5))
dataset.columns = [
    "led_power",
    "sun_position",
]
dataset.index.name = "date"
# mark all NA values with 0
dataset["led_power"].fillna(0, inplace=True)
# drop the first 24 hours
dataset = dataset[24:]
# summarize first 5 rows
print(dataset.head(5))
# save to file
dataset.to_csv("data/data.csv")
