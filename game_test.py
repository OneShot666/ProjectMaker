from math import *
from random import *
from time import *
from webcolors import name_to_rgb
from pathlib import Path
import datetime
import pygame
import os


# ! [v0.0.1] First tasks
# ! [v0.0.2] Second tasks
# ! [v1.0.0] Final tasks
class Main:                                                                     # Main class
    def __init__(self, name="Project name"):
        self.name = name
        self.creator = "One Shot"
        self.version = "v0.0.1"
        self.birthday = None
        # Initializers
        pygame.init()
        pygame.display.init()
        pygame.mixer.init()
        pygame.font.init()
        # Booleans data
        self.running = True
        # [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_size = self.screen.get_size()
        pygame.display.set_caption(self.name)
        # Fonts data
        self.Fonts = []
        self.FontSizes = {"small": 25, "middle": 40, "big": 50, "giant": 80}
        self.font_name = None
        self.main_font = None
        # File data
        # self.path = os.getcwd()
        self.path = Path(__file__).parent                                       # Current programm path
        self.Files = ["data", "fonts", "images", "musics", "saves", "sounds"]
        # Game data
        self.pressed = pygame.key.get_pressed()
        self.mouse = pygame.mouse.get_pos()
        self.horloge = pygame.time.Clock()
        self.left_click = False
        self.fps = 60
        # Colors data
        # self.bg_color = name_to_rgb("white")
        self.bg_color = name_to_rgb("lightgrey")
        self.borders_color = name_to_rgb("black")
        self.font_color = name_to_rgb("black")
        self.Colors = (name_to_rgb("red"), name_to_rgb("orange"), name_to_rgb("yellow"),
                       name_to_rgb("green"), name_to_rgb("cyan"), name_to_rgb("blue"),
                       name_to_rgb("purple"), name_to_rgb("deeppink"), name_to_rgb("brown"))
        # Timers data
        self.current_time = time()
        self.first_timer = time()
        self.first_duration = 10
        # Sounds data
        self.volume = 0.5
        self.Sounds = []
        self.sound1 = None
        # Main function
        self.first_launch_game()
        self.run()

    @staticmethod
    def get_current_date():
        return datetime.datetime.now().strftime("%d/%m/%Y")

    def first_launch_game(self):
        self.create_files()
        self.look_for_birthday()
        self.fill_data_lists()
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

    def fill_data_lists(self):                                                  # Fill game lists with data from files
        self.Fonts = [_ for _ in os.listdir(f"{self.path}/fonts") if _.endswith(".ttf")]
        if len(self.Fonts) > 0:
            self.font_name = self.Fonts[0]
            font_path = f"{self.path}/fonts/{self.font_name}"
        else:
            self.font_name = None
            font_path = None
        self.main_font = pygame.font.Font(font_path, 80)

        self.Sounds = [_ for _ in os.listdir(f"{self.path}/sounds") if _.endswith(".mp3")]
        if len(self.Sounds) > 0:
            self.sound1 = pygame.mixer.Sound(f"{self.path}/sounds/{self.Sounds[0]}.mp3")
            self.sound1.set_volume(self.volume)

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
        while self.running:                                                     # While playing
            self.current_time = time()
            self.pressed = pygame.key.get_pressed()
            self.mouse = pygame.mouse.get_pos()
            self.left_click = False

            for event in pygame.event.get():                                    # Get keyboard events
                if event.type == pygame.QUIT:
                    self.Close_game()

                if event.type == pygame.MOUSEBUTTONDOWN:                        # If left click
                    if event.button == 1:
                        self.left_click = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        self.Close_game()

            self.screen.fill(self.bg_color)

            self.greetings()

            pygame.display.flip()                                               # Update window
            self.horloge.tick(self.fps)

    def set_font_size(self, new_size=30):
        font_path = f"{self.path}/fonts/{self.font_name}" if self.font_name else None
        self.main_font = pygame.font.Font(font_path, new_size)

    def greetings(self):
        self.set_font_size(self.FontSizes["giant"])
        text = self.main_font.render(f"{self.name}", True, self.font_color)
        size = text.get_size()
        pos = (int(self.screen_size[0] * 0.5 - size[0] * 0.5),
               int(self.screen_size[1] * 0.4 - size[1] * 0.5))
        self.screen.blit(text, pos)

        self.set_font_size(self.FontSizes["big"])
        text = self.main_font.render(f"Made by {self.creator}", True, self.font_color)
        size = text.get_size()
        pos = (int(self.screen_size[0] * 0.5 - size[0] * 0.5),
               int(self.screen_size[1] * 0.5 - size[1] * 0.5))
        self.screen.blit(text, pos)

        self.set_font_size(self.FontSizes["middle"])
        text = self.main_font.render(f"{self.version}", True, self.font_color)
        size = text.get_size()
        pos = (int(self.screen_size[0] - size[0] * 1.1),
               int(self.screen_size[1] - size[1] * 1.1))
        self.screen.blit(text, pos)
        text = self.main_font.render(f"Fait le {self.birthday}", True, self.font_color)
        size = text.get_size()
        pos = (int(size[0] * 0.1), int(self.screen_size[1] - size[1] * 1.1))
        self.screen.blit(text, pos)

        self.set_font_size(self.FontSizes["small"])
        text = self.main_font.render(f"{self.volume}", True, self.font_color)
        size = text.get_size()
        pos = (int(self.screen_size[0] - size[0] * 1.1),
               int(self.screen_size[1] * 0.5 - size[1] * 0.5))
        self.screen.blit(text, pos)

    def Close_game(self):                                                       # Exit program
        pygame.time.delay(200)
        self.running = False
        pygame.quit()
        quit()


if __name__ == "__main__":
    main = Main()
