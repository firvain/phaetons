import pandas as pd
import argparse
from os import path
from colorama import Fore, Back, init

init(autoreset=True)

__author__ = "Evangelos Tsipis"
__version__ = "1.0.0"
__license__ = "MIT"


def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]", description="Format Data For LSTM.",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"v{__version__}",
    )
    parser.add_argument("file", nargs="*", help="filename")
    return parser


def format(fname):
    print(fname)
    dataset = pd.read_csv(fname, index_col=0)
    dataset.index.name = "date"
    print(dataset.head())
    cols = list(dataset.columns.values)
    # print(cols.pop())
    cols.insert(0, cols.pop())
    # cols.pop()
    dataset = dataset.loc[:, cols]
    dataset.to_csv(fname)


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    if not args.file:
        print(
            Back.RED + Fore.WHITE +
            f"{parser.prog}: Input File is required!!!"
        )
        exit()
    try:
        fname = args.file[0]
        if path.isfile(fname):
            format(fname)
        else:
            raise NameError("File Does not exist")
    except NameError as err:
        print(Back.RED + Fore.WHITE + f"{parser.prog}: {fname}: {err}")
