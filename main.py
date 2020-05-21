"""
Module Docstring
"""
import datetime
from colorama import Fore, Back, init

from neuralNetwork import getPl, getPls, getPpv, getPw
from battery import MinCapacity, Capacity
from calculations import CalcPdis, CalcPlsl, CalcPwpv
from export import createPandas  # ,  head
import calendar
from db import insertJson
from pylons import pylons

init(autoreset=True)

__author__ = "Evangelos Tsipis"
__version__ = "1.0.0"
__license__ = "MIT"


def decideOnBaterryCapacity(Cbat, CbatMin, Pwpv, Plsl):
    print(Cbat, CbatMin, Pwpv, Plsl)
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


def chechConditions(t, Pwpv, Plsl, CbatMin, Pl, Pls, Try=0):
    v = dict()
    if Pwpv > Plsl and Pwpv > 0 and Plsl > 0:

        print(Fore.MAGENTA + "CASE 1")
        input("Press Enter to continue...")
        print(t, Pwpv, Plsl, CbatMin, Pl, Pls)
        Cbat = Capacity(t)
        d = decideOnBaterryCapacity(Cbat, CbatMin, Pwpv, Plsl)

        if d["code"] != 2:
            b = dict()
            b["case"] = "case1"
            v = {**b, **d}
            return v
        print(Back.RED + Fore.WHITE + "New TRY")
        return chechConditions(t, Pwpv, Plsl, CbatMin, Pl, Pls)

    elif Pwpv < Plsl and Pwpv > 0 and Plsl > 0:
        print(Fore.MAGENTA + "CASE2")
        input("Press Enter to continue...")
        v["case"] = "case2"
        v["code"] = float("NaN")
        v["msg"] = ""
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
            print(v)
            return v
        else:
            if Try == 0:
                print(Fore.RED + "Try {}".format(Try))
                Pls = 0
                Plsl = CalcPlsl(Pl, Pls)
                Try = 1
                return chechConditions(t, Pwpv, Plsl, CbatMin, Pl, Pls, Try)
            elif Try == 1:
                print(Fore.RED + "Try {}".format(Try))
                Pl = 0.99 * Pl  # θέσε τον φωτισμό σε κατάσταση Dimming 80%
                Plsl = CalcPlsl(Pl, Pls)
                Try = 2
                return chechConditions(t, Pwpv, Plsl, CbatMin, Pl, Pls, Try)
            elif Try == 2:
                print(Fore.RED + "Try {}".format(Try))
                Pl = 0.6 * Pl  # θέσε τον φωτισμό σε κατάσταση Dimming 60%
                Plsl = CalcPlsl(Pl, Pls)
                Try = 3
                return chechConditions(t, Pwpv, Plsl, CbatMin, Pl, Pls, Try)

            v["code"] = 4
            v["msg"] = "Use Power from the GRID"
            v["GRID"] = "ON"
            v["LED"] = "ON"
            v["LOAD STATION"] = "ON"
            print(v)
            return v

    elif Pwpv == 0 and Plsl > 0:
        print(Fore.MAGENTA + "CASE3")
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
        print(Fore.MAGENTA + "CASE4")
        input("Press Enter to continue...")
        v["case"] = "case4"
        v["code"] = 6
        v["msg"] = ""
        v["GRID"] = float("NaN")
        v["LED"] = float("NaN")
        v["LOAD STATION"] = float("NaN")
        v["value"] = float("NaN")

        return v
    else:
        print(Fore.MAGENTA + "CASE5")
        v["code"] = 7
        v["msg"] = "Battery Capacity Unchanged"
        v["GRID"] = float("NaN")
        v["LED"] = float("NaN")
        v["LOAD STATION"] = float("NaN")
        v["value"] = float("NaN")
        return v


def main():
    """ Main entry point of the app """
    pylon = list(filter(lambda pylon: pylon["id"] == "2", pylons))

    results = list()
    today = datetime.datetime.now().date()
    todayIso = datetime.datetime.now().date().isoformat()
    print(todayIso)
    print(
        "Current Year: {}".format(today.year)
        + " is leap: {}".format(calendar.isleap(today.year))
    )
    for t in range(24):
        trynum = 0
        CbatMin = MinCapacity()
        Pw = getPw(t)
        Ppv = getPpv(t)
        Pwpv = CalcPwpv(Pw, Ppv)

        Pl = getPl(t)
        Pls = getPls(t)
        Plsl = CalcPlsl(Pl, Pls)

        results.append(t)
        results.append(pylon)
        results.append(
            datetime.datetime(
                today.year,
                today.month,
                today.day,
                t,
                tzinfo=datetime.timezone.utc,
            )
        )
        results.append(Pw)
        results.append(Ppv)
        results.append(Pwpv)
        results.append(Pl)
        results.append(Pls)
        results.append(Plsl)
        print(
            Back.LIGHTGREEN_EX + Fore.BLACK + "Step: {}".format(t),
            Fore.BLUE + "Pwpv: {}".format(Pwpv),
            Fore.CYAN + "Plsl: {}".format(Plsl),
            Fore.MAGENTA + "CbatMin: {}".format(round(CbatMin, 4) * 100),
        )
        recommendations = chechConditions(
            t, Pwpv, Plsl, CbatMin, Pl, Pls, trynum
        )
        print("REC")
        print()
        print(recommendations)
        print()
        # while case["code"] == 2:
        #     print(Back.RED + Fore.WHITE + "New TRY")
        #     case = chechConditions(t, Pwpv, Plsl, CbatMin, Pl, Pls, trynum)
        #     print(case)
        results.append(recommendations)
        # print(results)

    calcV = createPandas(results)
    print(calcV)
    # head(calcV)
    if len(calcV.index) == 24:
        insertJson(calcV.to_dict("records"))

    # print(calcV.iloc[0]["datetime"].isoformat())


if __name__ == "__main__":
    """ This is executed when run from the command line """

    main()
