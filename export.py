import pandas as pd
import numpy as np


def createPandas(
    result, cols=["pylon", "datetime", "Pw", "Ppv", "Pwpv", "Pl", "Pls",
                  "Plsl", "recommendations"]
):
    return pd.DataFrame(
        data=np.asarray(result).reshape(24, 10)[:, 1:10],
        columns=cols,
        index=np.asarray(result).reshape(24, 10)[:, 0],
    )


def head(p, n=5):
    print(p.head(n))
    return
