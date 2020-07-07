import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()
STEPS = os.getenv("STEPS")
if STEPS is not None:
    STEPS = int(STEPS)
else:
    STEPS = 24


def createPandas(
    result,
    cols=[
        "pylon",
        "datetime",
        "Pw",
        "Ppv",
        "Pwpv",
        "Pl",
        "Pls",
        "Plsl",
        "recommendations",
    ],
):
    return pd.DataFrame(
        data=np.asarray(result).reshape(STEPS, 10)[:, 1:10],
        columns=cols,
        index=np.asarray(result).reshape(STEPS, 10)[:, 0],
    )


def head(p, n=5):
    print(p.head(n))
    return
