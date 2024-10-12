from math import *
from random import *
from time import *
from pathlib import Path
import shutil
import stat
import os


def get_last_path():
    directory = Path(__file__).parent
    path = os.path.join(directory, "data", 'last_path.txt')
    if not os.path.exists(path):                                                # If file doesn't exist, create it
        open(path, 'w').close()
    with open(path, 'r') as path_file:
        last_path = path_file.read()
        path_file.close()
    return last_path


def is_path_dangerous(path):                                                    # Check if the path is vital for OS
    # List of critical paths for Windows
    DangerousPath = ["C:\\", "C:\\Windows", "C:\\Windows\\System32",
        "C:\\Program Files", "C:\\Program Files (x86)", "C:\\Users",
        "C:\\Documents and Settings", "C:\\ProgramData", "C:\\boot.ini",
        "C:\\pagefile.sys", "C:\\hiberfil.sys", "C:\\System Volume Information"]

    return path in DangerousPath


def remove_readonly(function, path, third_arg):
    os.chmod(path, stat.S_IWRITE)                                               # Remove read-only permissions
    function(path)


def remove_all_files(path):
    add_fail = False
    ToDelete = ["data", "fonts", "images", "musics", "saves", "sounds"]
    print(f"Deleting files in '{path}'...")
    for file in ToDelete:
        if os.path.exists(f"{path}/{file}"):
            try:
                shutil.rmtree(f"{path}/{file}")
            except PermissionError:
                print(f"Error: Program doesn't have permission to delete '{file}' !")
                print("Attempt to obtain admin rights...")
                try:
                    os.chmod(f"{path}/{file}", 0o777)
                    shutil.rmtree(f"{path}/{file}")
                    print(f"Admin right obtained successfully !")
                except PermissionError:
                    print(f"Attempt failed !")
                    print("Trying second delete method...")
                    try:
                        os.rmdir(f"{path}/{file}")
                        print(f"Empty directory '{file}' deleted successfully !")
                    except PermissionError:
                        print(f"Directory '{file}' isn't empty !")
                        add_fail = True
    return add_fail


def unmake_local_project():                                                     # Delete new project files if launch locally
    ToDelete = ["fonts", "images", "musics", "saves", "sounds"]
    directory = Path(__file__).parent
    for file in ToDelete:
        if os.path.exists(f"{directory}/{file}"):
            shutil.rmtree(f"{directory}/{file}")


def unmake_last_project():                                                      # Delete new project files at last known location
    last_path = get_last_path()
    if last_path is None or last_path == "":                                    # Stop function if no path found
        print("Last project doesn't exists or wasn't saved !")
        return
    print(f"Removing project in '{last_path}'...")
    try:                                                                        # Try to remove all project at once
        shutil.rmtree(last_path, onerror=remove_readonly)
        print(f"Project in '{last_path}' deleted successfully !")
    except PermissionError:
        print(f"Error: Program doesn't have permission to delete main directory '{last_path}' !")
        print("Trying second delete method...")
        try:                                                                    # Empty project first then delete it
            remove_all_files(last_path)
            os.rmdir(last_path)
            print(f"Project in '{last_path}' deleted successfully !")
        except PermissionError:
            print(f"Project directory '{last_path}' isn't empty !")


if __name__ == "__main__":
    # unmake_local_project()
    unmake_last_project()
