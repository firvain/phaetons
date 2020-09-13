import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('data\demokritos\weather_station_006fb28946c3bcb8.csv')

nyc_chart = sns.lineplot(
    x="time",
    y="temperature",
    data=data
).set_title('Temperature Over Time')
nyc_chart.get_figure().savefig("test.png")
