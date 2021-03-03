from typing import List
import numpy as np
from random import randint

from Matrix import Matrix
from input_helper import ForChunks

class Chunk:
    _origin: bool
    _value: str # path to npy


    def __init__(motherMatrix, azimuth, distance, width, length, origin=False)-> None:
        if azimuth < width: azimuth = width
        if distance < length: distance = length

        self._value = motherMatrix[azimuth - width:azimuth + width, \
        distance - length, distance + length]


class Chunks:
    WIDTH_OF_TARGET = 90
    LENGTH_OF_TARGET = 5
    _motherMatrix: Matrix
    _coordinates: List[int] # azimuth & distance in points

    _width: int
    _length: int

    _count: int
    _is_target: bool # target or stray

    # _chunks: List[Chunk]



    def __init__(self):
        self._getMatrix_and_coordinates()

        self._define_dimensions()

        self._define_type()

        self._load_chunks()




    def _getMatrix_and_coordinates(self) -> None:
        yn = {'1': 'Да', '2': 'Нет (Создать новую)'}
        print('Загрузить матрицу из БД?')
        for key in yn:
            print(f'{key} --> {yn[key]}')
        if input() == '1':

            db_matrixes = Matrix.fetch_db_matrixes()
            self._motherMatrix, self._coordinates = \
            ForChunks.choise_matrix_from_list(db_matrixes)
        else:
            motherMatrix = Matrix()
            self._motherMatrix = motherMatrix._name
            self._coordinates = motherMatrix._coordinates

    def _define_dimensions(self) -> None:
        yn = {'1': 'Да', '2': 'Нет'}
        print('Изменить размер снимка? По умолчанию 224*224')
        for key in yn:
            print(f'{key} --> {yn[key]}')
        if input() == '1':
            self._width, self._length = \
            ForChunks.set_dimensions_of_chunk()
        else:
            self._width = 224
            self._length = 224

    def _define_type(self):
        self._is_target = ForChunks.set_type_of_chunk()


    def _load_chunks(self):

        width_with_indent = Chunks.WIDTH_OF_TARGET - 20
        length_with_indent = Chunks.LENGTH_OF_TARGET + 10

        # distance нужны для генерации координат рандомных снимков
        distance_between_target_and_edge_width = self._width / 2 -\
        width_with_indent / 2

        distance_between_target_and_edge_length = self._length / 2 -\
        length_with_indent / 2
        if self._is_target:
            random_chunks_list = []
            if isinstance(self._coordinates[0], list):
                for i in self._coordinates:
                    current_azimuth = i[0]
                    current_distance = i[1]
                    random_chunks_list = __get_list_with_random_chunks(current_azimuth=current_azimuth, \
                    current_distance=current_distance, width=self._width, \
                    length=self._length)
            elif isinstance(self._coordinates[0], int):
                current_azimuth = self._coordinates[0]
                current_distance = self._coordinates[1]
                random_chunks_list = Chunks.__get_list_with_random_chunks(current_azimuth=current_azimuth, \
                current_distance=current_distance, width=self._width, \
                length=self._length)
            return random_chunks_list


    def get_list_with_random_chunks(self, current_azimuth, \
    current_distance, count_of_copy=5):


        origin_chunk = Chunk(motherMatrix=self._motherMatrix, azimuth=current_azimuth, distance=current_distance, \
        width=self._width, length=self._length, origin=True)

        random_chunks_list = [origin_chunk]

        for j in count_of_copy:

            new_azimuth = randint(current_azimuth -\
            distance_between_target_and_edge_width,\
            current_azimuth + distance_between_target_and_edge_width)

            new_distance = randint(current_distance-\
            distance_between_target_and_edge_length,\
            current_distance + distance_between_target_and_edge_length)

            random_chunk = Chunk(motherMatrix=self._motherMatrix, azimuth=new_azimuth, distance=new_distance, \
            width=self._width, length=self._length)

            random_chunks_list.append(random_chunk._value)

        return random_chunks_list



x = Chunks()
print(x._load_chunks())
print(x.__dict__)
