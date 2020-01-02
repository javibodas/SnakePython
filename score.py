# coding: utf-8
from json import load, dump, JSONDecodeError
from easygui import msgbox

__SCORE_FILE_NAME__ = 'score.json'
__SCORE_DEFAULT_STRUCTURE__ = '{"DATA":{"SNAKE":0,"NINGUNO":0}}'


class Score:

    def __init__(self, game):
    
        if not isinstance(game, str):
            raise ValueError("Parameter 'game' of Score class must be an string.")
            
        self._game = game
        self._max_points = 0
        self._points = 0
        self._data = {}
    
    @property
    def points(self):
        return self._points
        
    @property
    def max_points(self):
        return self._max_points
    
    @points.setter
    def points(self, points):
        self._points = points
    
    @max_points.setter
    def max_points(self, max_points):
        self._max_points = max_points
        

    def write_score_file(self):
    
        if self._points > self._max_points:
            self._max_points = self._points

            file_max_points = int(self._data['DATA'][self._game])
            self._data['DATA'][self._game] = self._max_points

            if self._max_points > file_max_points:
                try:
                    file = open(__SCORE_FILE_NAME__,'w')
                except FileNotFoundError:
                    file = open(__SCORE_FILE_NAME__, 'x')
                    file.write(__SCORE_DEFAULT_STRUCTURE__)

                dump(self._data, file)

    def read_score_file(self):
    
        file = None

        try:
            file = open(__SCORE_FILE_NAME__)
        except FileNotFoundError:
            file = open(__SCORE_FILE_NAME__, 'x')
            file.write(__SCORE_DEFAULT_STRUCTURE__)
            file = open(__SCORE_FILE_NAME__, 'r')

        try:
            self._data = load(file)
        except JSONDecodeError:
            file = open(__SCORE_FILE_NAME__, 'w')
            file.write(__SCORE_DEFAULT_STRUCTURE__)
            file = open(__SCORE_FILE_NAME__, 'r')
            self._data = load(file)

        self._max_points = int(self._data['DATA'][self._game])

