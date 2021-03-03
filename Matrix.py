from typing import List, Tuple
import numpy as np
import re

import db
from input_helper import ForMatrixes

class Matrix:
    _path: str
    _name: str
    _label: str

    _value: str  # path to npy
    _coordinates: str  # path to npy

    def __init__(self):
        # if _load_from_db(self):
        #     return

        self._load_label()
        self._load_path()
        self._load_name()

        self._load_value()
        self._load_coordinates()

        db.insert('matrixes', {'name': self._name, \
        'label': self._label, 'path': self._path, \
        'coordinates': self._coordinates, 'value': self._value})


    def _load_label(self) -> None:  # BI or SO or SN or SI
        self._label = ForMatrixes.set_label_of_cache()

    def _load_path(self) -> None:  # path to cache
        self._path = ForMatrixes.set_path_of_cache(self._label)

    def _load_name(self) -> None:  # name of cache

        self._name = ForMatrixes.set_name_of_cache(self._path)

    def _load_value(self) -> None:  # path to created npy with matrix
        raw = Matrix.__strings_from_cash(self._path + '/' + self._name + '.txt')
        f = Matrix.__parse_gen_BI if self._label == 'BI' \
        else Matrix.__parse_gen
        res = []
        print('Загрузка матрицы...')
        for i in f(raw):
            if self._label != 'BI':
                i[1] = i[1].split(' ')
            i[1] = list(filter(None, i[1]))
            i[1] = list(map(int, i[1]))
            res.append(i[1])
        self._value = self.save_npy(np.array(res).transpose())


    def _load_coordinates(self) -> str:  # path to npy with coordinates
        """Запрашивает и конвертирует координаты цели для кэша,
         полученного на вход"""
        list_with_input_coordinates = ForMatrixes.get_coordinates_for_cache(self._name)
        list_of_coordinates = []
        for i in list_with_input_coordinates:
            x, y = Matrix.kilometers_and_grades_to_coordinates(i[0], i[1])
            list_of_coordinates.append([x, y])
        if len(list_of_coordinates) == 1:
            list_of_coordinates = list_of_coordinates[0]
        self._coordinates = self.save_npy(np.array(list_of_coordinates), True)


    @staticmethod
    def __strings_from_cash(path) -> str:
        strings = ''
        with open(path, 'r') as f:
            for line in f:
                strings += line
            return strings

    @staticmethod
    def __parse_gen(raw):
        """Получает строку с сырым кэшем. Построчно генерирует
        содержащуюся в нём матрицу"""
        list_of_strings = re.findall(r"\d+\s*:[^\n]*", raw)
        for string in list_of_strings:
            yield string.split(':')

    @staticmethod
    def __parse_gen_BI(raw):
        """Получает строку с сырым кэшем. Построчно генерирует
        содержащуюся в нём матрицу. Только для бинарных кэшей
        (BI) """
        list_of_strings = re.findall(r"\d+\s*:[^\n]*", raw)
        for string in list_of_strings:
            yield string.replace(' ', '').split(':')

    @staticmethod
    def kilometers_and_grades_to_coordinates(grades, kilometers):
        """Получает на вход градусы и километры, возвращает
         преобразованные для разрешения кэша значения"""
        result_of_grades = int(grades * 2048 / 360)
        result_of_kilometers = int(kilometers * 1200 / 360)
        return result_of_grades, result_of_kilometers

    def save_npy(self, value, coordinates=False) -> str:  # return path of numpy array
        path = ForMatrixes.get_path_for_npy()
        temp = path + '/' + self._name
        if coordinates:
            temp += '_coordinates'
        np.save(temp, value)
        return path


    @staticmethod
    def delete_by_name(key: str) -> None:
        """get name of matrix to remove from db"""
        db.delete('matrixes', 'name', key)

    @staticmethod
    def fetch_db_matrixes() -> List[Tuple]:
        result = []
        temp = db.fetchall('matrixes', ['name', 'coordinates'])
        for i in temp:
            d = {'name': i['name'], 'coordinates': \
            Matrix.cooridnates_from_db(i['coordinates'] + '/' + i['name'])}
            result.append(d)
        return result

    @staticmethod
    def cooridnates_from_db(path: str) -> np.ndarray:
        try:
            result = np.load(path + '_coordinates.npy')
            return result
        except FileNotFoundError as e:
            print('Отсутствует файл с координатами')
            print(path)

# x = Matrix()
