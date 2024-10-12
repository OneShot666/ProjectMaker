from math import *
from random import *
from time import *
from pathlib import Path
import os


def main():
    # path = os.getcwd()
    path = Path(__file__).parent
    # path = "ProjectMaker/data"
    project = os.path.basename(path)
    abs_path = os.path.abspath(path)
    print(f"Chemin de base : {path}")
    print(f"Chemin absolu :  {abs_path}")
    print(f"Nom projet : {project}")


if __name__ == "__main__":
    main()
