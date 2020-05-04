import numpy as np


def CalcPwpv(Pw, Ppv):
    return Pw + Ppv


def CalcPlsl(Pl, Pls):
    return Pl + Pls


def CalcPdis(t):
    return (np.random.rand(1) * np.random.randint(1, 100))[0]
