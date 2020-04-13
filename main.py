"""
Module Docstring
"""
import datetime
import numpy as np

from colorama import Fore, Back, init

import pandas as pd

init(autoreset=True)

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"




def CalcPw(t):
    return (np.random.rand(1) * np.random.randint(1, 100))[0]


def CalcPpv(t):
    return (np.random.rand(1) * np.random.randint(1, 100))[0]


def CalcPwpv(Pw, Ppv):
    return Pw + Ppv


def CalcPl(t):
    return (np.random.rand(1) * np.random.randint(1, 100))[0]


def CalcPls(t):
    return (np.random.rand(1) * np.random.randint(1, 100))[0]


def CalcPlsl(Pl, Pls):
    return Pl + Pls


def CalcBatteryCapacity(t):
    return np.random.rand(1)[0]


def decideOnBaterryCapacity(Cbat, CbatMin, Pwpv, Plsl):
    a = dict()
    if Cbat == 1.0:
        a["code"] = 0
        a["msg"] = "Extra Power to GRID"
        a["GRID"] = float("NaN")
        a["LED"] = float("NaN")
        a["LOAD STATION"] = float("NaN")
        a["value"] = Pwpv
    elif Cbat > CbatMin or Cbat == CbatMin:
        Pch = Pwpv - Plsl

        a["code"] = 1
        a["msg"] = "Charge Battery"
        a["GRID"] = float("NaN")
        a["LED"] = float("NaN")
        a["LOAD STATION"] = float("NaN")
        a["value"] = Pch
    elif Cbat < CbatMin:
        a["code"] = 2
        a["msg"] = "Error"
        a["GRID"] = float("NaN")
        a["LED"] = float("NaN")
        a["LOAD STATION"] = float("NaN")
        a["value"] = float("NaN")
    return a


def CalcPdis(t):
    return (np.random.rand(1) * np.random.randint(1, 100))[0]


def chechConditions(t, Pwpv, Plsl, CbatMin, Pl, Pls, Try = 0):
    v = dict()


    if Pwpv > Plsl and Pwpv > 0 and Plsl > 0:
        print("case1")
        input("Press Enter to continue...")
        Cbat = CalcBatteryCapacity(t)
        d = decideOnBaterryCapacity(Cbat, CbatMin, Pwpv, Plsl)
        if d["code"] == 2:
            print(Back.RED + Fore.WHITE + "New TRY")
            chechConditions(t, Pwpv, Plsl, CbatMin, Pl, Pls)
        b = dict()
        b["case"] = "case1"
        v = {**b, **d }
        return v
    elif Pwpv < Plsl and Pwpv > 0 and Plsl > 0:
        print("case2")
        input("Press Enter to continue...")
        v["case"] = "case2"
        v["GRID"] = float("NaN")
        v["LED"] = float("NaN")
        v["LOAD STATION"] = float("NaN")
        v["value"] = float("NaN")

        Plsl_new = Plsl - Pwpv
        Pdis = CalcPdis(t)

        if Pdis >= Plsl_new:  # Αποφόρτιση μπαταρίας
            Plsl = Pdis
            v["msg"] = "Discharge Battery"
            v["code"] = 3
            v["value"] = Pdis
        else:
            if Try == 0:
                print(Fore.RED + "Try {}".format(Try))
                Pls = 0
                Plsl = CalcPlsl(Pl, Pls)
                Try = 1
                chechConditions(t, Pwpv, Plsl, CbatMin, Pl, Pls, Try)
            elif Try == 1:
                print(Fore.RED + "Try {}".format(Try))
                Pl = 0.99 * Pl  # θέσε τον φωτισμό σε κατάσταση Dimming 80%
                Plsl = CalcPlsl(Pl, Pls)
                Try = 2
                chechConditions(t, Pwpv, Plsl, CbatMin, Pl, Pls, Try)
            elif Try == 2:
                print(Fore.RED + "Try {}".format(Try))
                Pl = 0.6 * Pl  # θέσε τον φωτισμό σε κατάσταση Dimming 60%
                Plsl = CalcPlsl(Pl, Pls)
                Try = 3
                chechConditions(t, Pwpv, Plsl, CbatMin, Pl, Pls, Try)

            v["code"] = 4
            v["msg"] = "Use Power from the GRID"
            v["GRID"] = "ON"
            v["LED"] = "ON"
            v["LOAD STATION"] = "ON"

        return v

    elif Pwpv == 0 and Plsl > 0:
        print("case3")
        input("Press Enter to continue...")
        v["case"] = "case2"
        v["code"] = 5
        v["msg"] = ""
        v["GRID"] = float("NaN")
        v["LED"] = float("NaN")
        v["LOAD STATION"] = float("NaN")
        v["value"] = float("NaN")

        return v
    elif Pwpv > 0 and Plsl == 0:
        print("case4")
        input("Press Enter to continue...")
        v["case"] = "case4"
        v["code"] = 5
        v["msg"] = ""
        v["GRID"] = float("NaN")
        v["LED"] = float("NaN")
        v["LOAD STATION"] = float("NaN")
        v["value"] = float("NaN")

        return v
    else:
        return "Battery Capacity Unchanged"


def main():
    """ Main entry point of the app """
    v = list()
    today = datetime.datetime.now().date()

    for t in range(24):
        trynum = 0
        CbatMin = 0.15
        Pw = CalcPw(t)
        Ppv = CalcPpv(t)
        Pwpv = CalcPwpv(Pw, Ppv)

        Pl = CalcPl(t)
        Pls = CalcPls(t)
        Plsl = CalcPlsl(Pl, Pls)

        v.append(datetime.datetime(today.year, today.month, today.day, t))
        v.append(t)
        v.append(Pw)
        v.append(Ppv)
        v.append(Pwpv)
        v.append(Pl)
        v.append(Pls)
        v.append(Plsl)
        print(
            Back.LIGHTGREEN_EX + Fore.BLACK + "Step: {}".format(t),
            Fore.BLUE + "Pwpv: {}".format(Pwpv),
            Fore.CYAN + "Plsl: {}".format(Plsl),
            Fore.MAGENTA + "CbatMin: {}".format(round(CbatMin, 4) * 100),
        )
        case = chechConditions(t, Pwpv, Plsl, CbatMin, Pl, Pls, trynum)
        print(case)
        # while case["code"] == 2:
        #     print(Back.RED + Fore.WHITE + "New TRY")
        #     case = chechConditions(t, Pwpv, Plsl, CbatMin, Pl, Pls, trynum)
        #     print(case)
        v.append(case)

    calcV = pd.DataFrame(
        data=np.asarray(v).reshape(24, 9)[:, 1:9],
        columns=["Step", "Pw", "Ppv", "Pwpv", "Pl", "Pls", "Plsl", "case"],
        index=np.asarray(v).reshape(24, 9)[:, 0],
    )
    # print(calcV.head(5))


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
