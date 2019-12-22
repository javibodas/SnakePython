# coding: utf-8
from json import load, dump, JSONDecodeError
from easygui import msgbox

SCORE_FILE_NAME = 'score.json'
SCORE_DEFAULT_STRUCTURE = '{"DATA": {"SNAKE": 0,"NINGUNO": 0}}'


class Score:
    def __init__(self, game):
        self.max_points = 0
        self.points = 0
        self._data = {}

        if not isinstance(game, str):
            raise ValueError("Parameter 'game' of Score class must be an string.")
        self._game = game

    def get_points(self):
        return self.points

    def get_max_points(self):
        return self.max_points

    def set_points(self, points):
        self.points = points

    def set_max_points(self, max_points):
        self.max_points = max_points

    def set_data(self, data):
        self._data = data

    def get_data(self):
        return self._data

    def write_score_file(self):
        if self.points > self.max_points:
            self.max_points = self.points

            file_max_points = int(self._data['DATA'][self._game])
            self._data['DATA'][self._game] = self.max_points

            if self.max_points > file_max_points:
                try:
                    file = open(SCORE_FILE_NAME,'w')
                except FileNotFoundError:
                    file = open(SCORE_FILE_NAME, 'x')
                    file.write(SCORE_DEFAULT_STRUCTURE)
                except E as e:
                    msgbox('There was an error writing score game.\n ' + type(e))
                    exit(1)

                dump(self._data, file)

    def read_score_file(self):
        file = None

        try:
            file = open(SCORE_FILE_NAME)
        except FileNotFoundError:
            file = open(SCORE_FILE_NAME, 'x')
            file.write(SCORE_DEFAULT_STRUCTURE)
        except E as e:
            msgbox('There was an error opening score file.\n ' + type(e))
            exit(1)

        try:
            self._data = load(file)
        except JSONDecodeError:
            file = open(SCORE_FILE_NAME, 'w')
            file.write(SCORE_DEFAULT_STRUCTURE)
            self._data = load(file)
        except E as e:
            msgbox('There was an error reading score file.\n ' + type(e))
            exit(1)

        self.max_points = int(self._data['DATA'][self._game])

