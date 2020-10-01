__version__ = "0.1"
__author__ = "Evangelos Tsipis"

import pandas as pd

from datetime import datetime, timezone
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


def profile_file(t):
    switcher = {
        "min": lambda: "Profile_Cmin.csv",
        "max": lambda: "Profile_Cmax.csv",
        "mean": lambda: "Profile_C_mean.csv",
    }
    func = switcher.get(t, lambda: "Invalid")
    return func()


def get_c_from_profile(
    profile_type="average", hour=None, month=None, vis=False
):
    """Finds C from fixed profile and returns it

    Args:
        profile_type (str, optional): [Type of profile file csv].
            Defaults to "average".
        hour ([str], optional): [hour to search]. Defaults to None.
        month ([str], optional): [month to search. Defaults to None.
        vis(bool, optional)" [Visualize month at time] Defaults to False.

    Returns:
        int: C value from profile
    """
    if hour is None or month is None:
        d = datetime.now(timezone.utc)
        hour = d.astimezone().strftime("%H:00:00")
        month = d.astimezone().strftime("%B")
    # try:
    file = profile_file(profile_type)
    if file == "Invalid":
        raise Exception("Invalid Profile Type")
    try:
        data_folder = Path("data/Profiles")
        filename = data_folder / file
        df = pd.read_csv(filename, header=0, index_col=0)
        if vis is True:
            sns.set_theme()
            sns.set_style("ticks")
            sns.scatterplot(
                data=df, x=df.index.values, y=df[month], hue=df[month]
            )
            plt.ylabel("C " + profile_type)
            plt.xticks(
                ticks=df.index.values[::3],
                rotation=45.0,
                horizontalalignment="right",
                fontweight="light",
                fontsize="x-small",
                rotation_mode="anchor",
            )
            # chart.set_xticklabels(chart.get_xticklabels(), rotation=45)
            # sns.set_xticklabels(step=5)
            plt.show()
        return df.loc[hour, month].astype(float)
    except (Exception, FileNotFoundError) as e:
        return e
