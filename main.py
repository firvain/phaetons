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


def CalcBatteryCapacity():
    return np.random.rand(1)[0]


def decideOnBaterryCapacity(Cbat, CbatMin, Pwpv, Plsl):
    a = dict()
    if Cbat == 1.0:
        a["msg"] = "Extra Power to Grid"
        a["code"] = 0
        a["value"] = Pwpv
    elif Cbat > CbatMin or Cbat == CbatMin:
        Pch = Pwpv - Plsl

        a["msg"] = "Charge Battery"
        a["code"] = 1
        a["value"] = Pch
    elif Cbat < CbatMin:
        a["msg"] = "Error"
        a["code"] = 2
        a["value"] = float("NaN")
    return a


def chechConditions(t, Pwpv, Plsl, CbatMin):
    print(
        Back.LIGHTGREEN_EX + Fore.BLACK + "Step: {}".format(t),
        Fore.BLUE + "Pwpv: {}".format(Pwpv),
        Fore.CYAN + "Plsl: {}".format(Plsl),
        Fore.MAGENTA + "CbatMin: {}".format(round(CbatMin, 4) * 100),
    )
    if Pwpv > Plsl and Pwpv > 0 and Plsl > 0:
        Cbat = CalcBatteryCapacity()
        decisionOnBattery = decideOnBaterryCapacity(Cbat, CbatMin, Pwpv, Plsl)
        print(Back.RED + "Battery Capacity: {}%".format(round(Cbat, 4) * 100))
        # if decisionOnBattery["code"] == 0: #Διοχέτευση της παραγόμενης ενέργειας στο δίκτυο ηλεκτρικής ενέργειας
        #     print(
        #         Fore.GREEN + decisionOnBattery["msg"],
        #         "=",
        #         Fore.BLUE
        #         + str(decisionOnBattery["value"]),
        #     )
        # elif decisionOnBattery["code"] == 1: #Φόρτιση μπαταρίας με ισχύ φόρτισης Pch(t) = PWPV(t) - PLSL(t)
        #     print(
        #         Fore.GREEN + decisionOnBattery["msg"],
        #         "with Power=",
        #         Fore.CYAN
        #         + str(decisionOnBattery["value"]),
        #     )
        # else: ##Error πήγαινε στο βήμα IΧ
        #     print(Fore.RED + decideOnBaterryCapacity(Cbat, CbatMin, Pwpv, Plsl)["msg"])
        decisionOnBattery["case"] = "case1"
        return decisionOnBattery
    elif Pwpv < Plsl and Pwpv > 0 and Plsl > 0:
        return "case2"
    elif Pwpv == 0 and Plsl > 0:
        return "case3"
    elif Pwpv > 0 and Plsl == 0:
        return "case4"
    else:
        return "Battery Capacity Unchanged"


def main():
    """ Main entry point of the app """
    v = list()
    today = datetime.datetime.now().date()
    for t in range(24):
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

        case = chechConditions(t, Pwpv, Plsl, 0.99)
        if len(case) == 4:
            print(case)
            while case["code"] == 2:
                print("New TRY")
                case = chechConditions(t, Pwpv, Plsl, 0.99)
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
