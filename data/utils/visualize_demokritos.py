import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

file_directory = Path("data/demokritos/resampled")
sns.set_theme()
sns.set_style("ticks")
df = pd.read_csv(
    file_directory / "weather_station_006fb28946c3bcb8.csv", index_col="time"
)
print(len(df))
# quit()
nyc_chart = sns.scatterplot(
    data=df[df.temperature < 1000], x=df[df.temperature < 1000].index.values, y=df[df.temperature < 1000].temperature
).set_title("Temperature Over Time")
plt.xticks(
    ticks=range(0, len(df.index)),
    # labels=df.index.values,
    rotation=45,
    horizontalalignment="right",
    fontweight="light",
    fontsize="x-small",
    rotation_mode="anchor",
)

# nyc_chart.get_figure().savefig("test.png")
plt.show()
