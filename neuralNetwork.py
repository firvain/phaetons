import numpy as np
from neural import LSTM_WindTurbine
from neural import LSTM_PvSystem
from neural import LSTM_LedSystem
from neural import LSTM_LoadStationSystem
from neural.example import LSTM


# WIND TURBINE SYSTEM functions
def predictPw(forecastHours, visualize):
    val = LSTM_WindTurbine.LSTM_RUN(
        "data/dummy/WindTurbine.csv", forecastHours, visualize
    )
    return val


def getPw(forecastHours):
    val = LSTM_WindTurbine.LSTM_RUN("data/dummy/WindTurbine.csv")
    return val


# PHOTOVOLTAIC SYSTEM functions
def predictPpv(forecastHours, visualize):
    val = LSTM_PvSystem.LSTM_RUN(
        "data/dummy/PvSystem.csv", forecastHours, visualize
    )
    return val


def getPpv(forecastHours):
    val = LSTM_PvSystem.LSTM_RUN("data/dummy/PvSystem.csv")
    return val


# LED SYSTEM functions
def predictPl(forecastHours, visualize):
    val = LSTM_LedSystem.LSTM_RUN(
        "data/dummy/LedSystem.csv", forecastHours, visualize
    )
    return val


def getPl(forecastHours):
    val = LSTM_LedSystem.LSTM_RUN(
        "data/dummy/LedSystem.csv"
    )
    return val


# POWER CONSUMPTION SYSTEM functions
def predictPls(forecastHours, visualize):
    val = LSTM_LoadStationSystem.LSTM_RUN(
        "data/dummy/LoadStationSystem.csv", forecastHours, visualize
    )
    return val


def getPls(forecastHours):
    val = LSTM_LoadStationSystem.LSTM_RUN("data/dummy/LoadStationSystem.csv")
    return val


# Example and Dummy
def example(forecastHours):
    return LSTM.LSTM_RUN("data/example/pollution.csv")


def dummyResult(forecastHours):
    return (np.random.rand(1) * np.random.randint(1, 100))[0]


def predictNeurals(forecastHours, visualize):
    Pw = predictPw(forecastHours, visualize)
    Ppv = predictPpv(forecastHours, visualize)
    Pl = predictPl(forecastHours, visualize)
    Pls = predictPls(forecastHours, visualize)
    return Pw, Ppv, Pl, Pls
