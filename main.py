from math import *
from random import *
from time import *
from pathlib import Path
import subprocess
import datetime
import sys
import os
import re

# ! Check with incorrect name and path (+ non-game type)
# ! Make test with os.path.abspath() (add path if just file name but is path correct ?)
# ! Add file in data/last_path.txt fill by main.py and use by unmaker.py
# ! Check if unmaker.py work


# [v0.0.1] Have most of main variables (version, date of creation, path)
# [v0.0.2] Have most of main functions (start, save, run, quit)
# [v0.0.3] Make function to create an all new project with a given name in a given path
# [v0.0.4] Make function to use text files in src and complete programs inn new project
# [v0.0.5] Make function to run main program of new project
# [v0.0.6] Ask player name, path and if project is game when launching
# [v0.0.7] Check if data enterez by user are valid
# ! [v0.0.8] In new project, make main.py auto-detect project name and update it
# ! [v0.0.9] Couple new project with Game_Idea_Maker ?
# ! [v0.1.0] Open new project with PyCharm
class Main:                                                                     # Main class
    def __init__(self, path_to_make=None, project_name=None, is_game=None):
        self.name = "Project maker"
        self.creator = "One Shot"
        self.version = "v0.0.7"
        self.birthday: str = None
        # File data
        # self.path = os.getcwd()
        self.path = Path(__file__).parent                                       # Current programm path
        self.Files = ["data", "src"]
        # Given data
        self.project_is_game: bool = is_game
        self.given_name: str = project_name
        self.given_path: str = path_to_make
        # Main function
        self.first_launch_game()
        self.run()

    @staticmethod
    def get_current_date():
        return datetime.datetime.now().strftime("%d/%m/%Y")

    @staticmethod
    def is_valid_filename(name):
        InvalidChars = r'[<>:"/\\|?*\x00-\x1f]'
        return not re.search(InvalidChars, name)

    def is_valid_directory_path(self, path):
        try:                                                                    # Check if valid path
            abs_path = os.path.abspath(path)                                    # Check if path can be turn into abspath
            is_valid = self.is_valid_filename(path)
            if not is_valid:
                return False
            return True
        except (OSError, ValueError, TypeError):                                # If path invalid
            return False

    def first_launch_game(self):
        self.create_files()
        self.look_for_birthday()
        self.save_game_data()

    def create_files(self):                                                     # Create files if doesn't exist
        for file in self.Files:
            path = f"{self.path}/{file}"
            if not os.path.exists(path):
                os.makedirs(path)
        with open(f"{self.path}/data/data.txt", 'w') as file:
            file.write("")

    def look_for_birthday(self):
        if self.birthday is None:                                               # If first launch
            with open(f"{self.path}/data/data.txt", 'r') as file:
                lines = file.readlines()
                birthday = lines[3].strip() if len(lines) >= 4 else None        # Check if data saved
            with open(f"{self.path}/data/data.txt", 'w') as file:
                self.birthday = self.get_current_date() if birthday is None else birthday

    def save_game_data(self):                                                   # Write most of the game data
        with open(f"{self.path}/data/data.txt", 'w') as file:
            file.write(self.name + "\n")
            file.write(self.creator + "\n")
            file.write(self.version + "\n")
            file.write(self.birthday + "\n")

    @staticmethod
    def modify_file_line(filename, line_number, text):
        with open(filename, 'r') as file:
            lines = file.readlines()

        if line_number <= len(lines):                                           # Modify line
            lines[line_number - 1] = text + '\n'
        else:
            lines.extend(['\n'] * (line_number - len(lines) - 1))               # Eventually add blank lines
            lines.append(text + '\n')                                           # End of file

        with open(filename, 'w') as file:                                       # Update
            file.writelines(lines)

    def run(self):                                                              # Main function
        self.greetings()
        self.ask_user_data()
        self.create_new_project()
        self.Close_program()

    def greetings(self):                                                        # Present project
        print(f"Bienvenue sur {self.name} ({self.version}) !")
        print(f"Ce programme permet de créer un projet dans un répertoire donné.")
        print(f"")

    def ask_user_data(self):                                                    # Personnalize new project
        while self.given_name is None:
            name = input(f"Entrez le nom de votre nouveau projet : ")
            if self.is_valid_filename(name):                                    # Check if name valid
                self.given_name = name
            else:
                print("Ce nom contient des caractères incorrects !")
        print("")
        print(f"Chemin par défaut : {self.path.parent}")
        while self.given_path is None:
            path = input("Entrez le chemin de votre nouveau projet (ENTRÉE pour chemin par défaut) : ")
            print(path.replace("\\", ""))  # !!!
            if path == "" or path is None:                                      # Default path
                self.given_path = self.path.parent
            elif self.is_valid_directory_path(path.replace("\\", "")):          # Check if path valid
                self.given_path = path
            else:
                print("Ce chemin n'est pas correct !")
        print("")
        if self.project_is_game is None:                                        # Ask if new project is a game
            game = input(f"Votre nouveau projet est-il un jeu (y/n) : ").lower()
            self.project_is_game = True if game == "y" else False

    def create_new_project(self):
        # Create project directory at given path
        project_path = f"{self.given_path}/{self.given_name}"
        if not os.path.exists(project_path):                                    # If dir doesn't exists, create it
            os.makedirs(project_path)

        # Create files at given path
        if self.project_is_game:                                                # Create project as game project
            filename = "main_game_class.txt"
            with open(os.path.join(self.path, "src", filename), 'r') as file:
                content = file.read()
            with open(os.path.join(project_path, 'main.py'), 'w') as new_file:
                new_file.write(content)
        else:                                                                   # Main program for classic project
            filename = "main_class.txt"
            with open(os.path.join(self.path, "src", filename), 'r') as file:
                content = file.read()
            with open(os.path.join(project_path, 'main.py'), 'w') as new_file:
                new_file.write(content)
            filename = "main_function.txt"
            with open(os.path.join(self.path, "src", filename), 'r') as file:
                content = file.read()
            with open(os.path.join(project_path, 'test.py'), 'w') as new_file:
                new_file.write(content)

        # Launch main file
        to_launch = os.path.join(project_path, 'main.py')                       # Will launch new made main program
        command = f'python "{to_launch}"'
        try:                                                                    # Use python directly
            subprocess.run(['python', to_launch], check=True)
        except subprocess.CalledProcessError:                                   # Use command on cmd
            os.system(command)

        print(f"Projet '{self.given_name}' créé à '{self.given_path}' avec succès !")

    @staticmethod
    def Close_program():                                                       # Exit program
        sys.exit()


if __name__ == "__main__":
    main = Main()
