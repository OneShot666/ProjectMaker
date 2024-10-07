from math import *
from random import *
from time import *
import os


def main():
    path = os.getcwd()
    abs_path = os.path.abspath(path)
    print(f"Chemin de base : {path}")
    print(f"Chemin absolu :  {abs_path}")


if __name__ == "__main__":
    main()
