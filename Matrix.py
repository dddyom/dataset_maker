from typing import List
import numpy as np
import glob
import os
import re

import db

class Matrix:
    _path: str
    _name: str
    _label: str

    _value: str  # path to npy
    _coordinates: str  # path to npy

    def __init__(self):
        # if _load_from_db(self):
        #     return

        self._label = self._load_label()
        self._path = self._load_path()
        self._name = self._load_name()

        self._value = self._load_value()
        self._coordinates = self._load_coordinates()

        db.insert('matrixes', {'name': self._name, \
        'label': self._label, 'path': self._path, \
        'coordinates': self._coordinates, 'value': self._value})

    @staticmethod
    def _load_label() -> str:  # BI or SO or SN or SI
        caches_dict = {'1': 'BI', '2': 'SO', '3': 'SN', '4': 'SI'}
        print('\nТип кэша: (ожидается индекс)')
        while True:
            for key in caches_dict:
                print(f'{key} --> {caches_dict[key]}')
            try:
                label = caches_dict[str(input())]
            except (UnboundLocalError, KeyError) as e:
                print(e, 'Ожидается индекс')
                continue
            return label

    def _load_path(self) -> str:  # path to cache
        while True:
            print(f'Путь до {self._label} кэша:')
            path = str(input())
            temp = path + f'/{self._label}*'
            try:
                list_of_caches = glob.glob(temp)
                if not list_of_caches:
                    raise ValueError
            except ValueError as e:
                print(f'Некорректный путь (Либо в папке отсутствует кэш в формате {self._label}*.txt)-->', temp)
                continue
            return path

    def _load_name(self) -> str:  # name of cache
        while True:
            print('Имя кэша с матрицей (индекс): ')
            for index, name in enumerate(os.listdir(self._path)):
                print(index, ' --> ', name)
            try:
                name = os.listdir(self._path)[int(input())]
            except (IndexError, TypeError, ValueError) as e:
                print(f'Ожидается индекс от 0 до {len(os.listdir(self._path))}')
                continue
            return name[:-4]

    def _load_value(self) -> str:  # path to created npy with matrix
        raw = Matrix.strings_from_cash(self._path + '/' + self._name + '.txt')
        f = Matrix.parse_gen_BI if self._label == 'BI' else Matrix.parse_gen
        res = []
        print('Загрузка матрицы...')
        for i in f(raw):
            if self._label != 'BI':
                i[1] = i[1].split(' ')
            i[1] = list(filter(None, i[1]))
            i[1] = list(map(int, i[1]))
            res.append(i[1])
        return self.save_npy(np.array(res))

    def _load_coordinates(self) -> str:  # path to npy with coordinates
        """Запрашивает и конвертирует координаты цели для кэша, полученного на вход"""
        int_data = []
        list_of_coordinates = []
        print(f"Азимут, дальность для цели"
              f"\n{self._name} "
              f"\nкэша в формате:"
              f"\nA1 D1"
              f"\nA2 D2")
        input_data = list(iter(input, ''))
        for i in input_data:
            int_data.append(list(map(int, i.split())))
        for i in int_data:
            x, y = Matrix.kilometers_and_grades_to_coordinates(i[0], i[1])
            list_of_coordinates.append([x, y])
        if len(list_of_coordinates) == 1:
            list_of_coordinates = list_of_coordinates[0]
        return self.save_npy(np.array(list_of_coordinates), True)

    # @staticmethod
    # def output():
    #     columns = db.fetchall('matrixes', ['path', 'name', 'coordinates', 'value'])
    #     for i in columns:
    #         print(i)


    @staticmethod
    def strings_from_cash(path) -> str:
        strings = ''
        with open(path, 'r') as f:
            for line in f:
                strings += line
            return strings

    @staticmethod
    def parse_gen(raw):
        """Получает строку с сырым кэшем. Построчно генерирует содержащуюся в нём матрицу"""
        list_of_strings = re.findall(r"\d+\s*:[^\n]*", raw)
        for string in list_of_strings:
            yield string.split(':')

    @staticmethod
    def parse_gen_BI(raw):
        """Получает строку с сырым кэшем. Построчно генерирует содержащуюся в нём матрицу. Только для бинарных кэшей
        (BI) """
        list_of_strings = re.findall(r"\d+\s*:[^\n]*", raw)
        for string in list_of_strings:
            yield string.replace(' ', '').split(':')

    @staticmethod
    def kilometers_and_grades_to_coordinates(grades, kilometers):
        """Получает на вход градусы и километры, возвращает преобразованные для разрешения кэша значения"""
        result_of_grades = int(grades * 2048 / 360)
        result_of_kilometers = int(kilometers * 1200 / 360)
        return result_of_grades, result_of_kilometers

    def save_npy(self, value, coordinates=False) -> str:  # return path of numpy array
        while True:
            print('Путь для сохранения матрицы в npy: ')
            path = str(input())
            try:
                if not os.path.isdir(path):
                    raise ValueError

                temp = path + '/' + self._name
                if coordinates:
                    temp += '_coordinates'

                np.save(temp, value)
            except ValueError as e:
                print('Некорректный путь -->', path)
                continue
            return path

    @classmethod
    def delete_by_name(name: str) -> None:
        """get name of matrix to remove from db"""
        db.delete('matrixes', 'name', {name})






print(Matrix.output())
