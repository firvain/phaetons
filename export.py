import pandas as pd
import numpy as np


def createPandas(
    result, cols=["datetime", "Pw", "Ppv", "Pwpv", "Pl", "Pls", "Plsl", "case"]
):
    return pd.DataFrame(
        data=np.asarray(result).reshape(24, 9)[:, 1:9],
        columns=cols,
        index=np.asarray(result).reshape(24, 9)[:, 0],
    )


def head(p, n=5):
    print(p.head(n))
    return
