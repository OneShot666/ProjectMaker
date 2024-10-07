from math import *
from random import *
from time import *
import shutil
import os


def unmaker_main_file():
    directory = Path(__file__).parent
    ToDelete = ["fonts", "images", "musics", "saves", "sounds"]
    for file in ToDelete:
        if os.path.exists(f"{directory}/{file}"):
            shutil.rmtree(f"{directory}/{file}")


if __name__ == "__main__":
    unmaker_main_file()
