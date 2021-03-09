import numpy as np
from random import randint
from typing import List, Dict, Union, Any

from Matrix import Matrix
import input_helper
import db


class Chunk:
    origin: bool
    value: str  # path to npy

    def __init__(self, mother_matrix_path, mother_matrix_name, azimuth, distance, width, length, origin=False) -> None:
        mother_matrix = np.load(mother_matrix_path + '/' + mother_matrix_name + '.npy')
        if azimuth < width:
            azimuth = width
        if distance < length:
            distance = length

        self.value = mother_matrix[azimuth - width:azimuth + width,
                     distance - length: distance + length]

        self.origin = origin


class Chunks:
    WIDTH_OF_TARGET = 90
    LENGTH_OF_TARGET = 5
    _motherMatrixPath: str
    _motherMatrixName: str
    _coordinates: str  # azimuth & distance in points

    _width: int
    _length: int

    _count: int
    _is_target: bool  # target or stray

    _chunks: List[Chunk]

    _value: str

    def __init__(self):
        self._get_matrix_and_coordinates()

        self._define_dimensions()

        self._define_type()

        self._define_count()

        self._load_chunks()

        self._load_path_to_chunks_array()

        db.insert('chunks', {'value': self._value,
                             'is_target': self._is_target,
                             'width': self._width, 'length': self._length,
                             'mother_matrix': self._motherMatrixName, 'dataset': ''})

    def _get_matrix_and_coordinates(self) -> None:
        yn = {'1': 'Да', '2': 'Нет (Создать новую)'}
        print('Загрузить матрицу из БД?')
        for key in yn:
            print(f'{key} --> {yn[key]}')
        if input() == '1':

            db_matrices = Matrix.fetch_db_matrices()
            self._motherMatrixPath, self._motherMatrixName, self._coordinates = \
                input_helper.ForChunks.choise_matrix_from_list(db_matrices)
        else:
            mother_matrix = Matrix()
            self._motherMatrixPath = mother_matrix.value
            self._motherMatrixName = mother_matrix.name
            self._coordinates = mother_matrix.coordinates

    def _define_dimensions(self) -> None:
        yn = {'1': 'Да', '2': 'Нет'}
        print('Изменить размер снимка? По умолчанию 224*224')
        for key in yn:
            print(f'{key} --> {yn[key]}')
        if input() == '1':
            self._width, self._length = \
                input_helper.ForChunks.set_dimensions_of_chunk()
        else:
            self._width = 224
            self._length = 224

    def _define_type(self):
        self._is_target = input_helper.ForChunks.set_type_of_chunk()

    def _define_count(self):
        self._count = input_helper.ForChunks.set_count_of_chunk()

    def _load_chunks(self):
        if self._is_target:
            random_chunks_list = []
            path_to_coordinates = self._coordinates + '/' + self._motherMatrixName + '_coordinates.npy'
            print(path_to_coordinates)
            coordinates = np.load(path_to_coordinates)
            if isinstance(coordinates[0], list):
                for i in coordinates:
                    current_azimuth = int(i[0])
                    current_distance = int(i[1])
                    random_chunks_list = self.__get_list_with_random_chunks(current_azimuth=current_azimuth,
                                                                            current_distance=current_distance,
                                                                            count_of_copy=self._count)
            elif isinstance(coordinates[0], np.int64):

                current_azimuth = int(coordinates[0])
                current_distance = int(coordinates[1])
                random_chunks_list = self.__get_list_with_random_chunks(current_azimuth=current_azimuth,
                                                                        current_distance=current_distance,
                                                                        count_of_copy=self._count)
            self._chunks = random_chunks_list

    def __get_list_with_random_chunks(self, current_azimuth,
                                      current_distance, count_of_copy=5):

        width_with_indent = Chunks.WIDTH_OF_TARGET - 20
        length_with_indent = Chunks.LENGTH_OF_TARGET + 10

        # distance нужны для генерации координат рандомных снимков
        distance_between_target_and_edge_width = int(self._width / 2 - width_with_indent / 2)

        distance_between_target_and_edge_length = int(self._length / 2 - length_with_indent / 2)

        print(self._motherMatrixPath)
        origin_chunk = Chunk(
            mother_matrix_path=self._motherMatrixPath,
            mother_matrix_name=self._motherMatrixName,
            azimuth=current_azimuth,
            distance=current_distance,
            width=self._width,
            length=self._length,
            origin=True
        )

        random_chunks_list = [origin_chunk]

        for j in range(count_of_copy):
            new_azimuth = randint(current_azimuth -
                                  distance_between_target_and_edge_width,
                                  current_azimuth + distance_between_target_and_edge_width)

            new_distance = randint(current_distance -
                                   distance_between_target_and_edge_length,
                                   current_distance + distance_between_target_and_edge_length)

            random_chunk = Chunk(
                mother_matrix_path=self._motherMatrixPath,
                mother_matrix_name=self._motherMatrixName,
                azimuth=new_azimuth,
                distance=new_distance,
                width=self._width,
                length=self._length,
            )
            random_chunks_list.append(random_chunk.value)

        return random_chunks_list

    def _load_path_to_chunks_array(self):
        path = input_helper.get_path_for_npy()
        self._value = path + '/' + self._motherMatrixName + '_' + str(self._count) + '.npy'
        np.save(self._value, np.array(self._chunks[1]))

    @staticmethod
    def fetch_db_chunks() -> List[Dict[str, Union[np.ndarray, Any]]]:
        result = []
        temp = db.fetchall('chunks', ['value', 'is_target', 'width', 'length'])
        for i in temp:
            d = {'value': i['value'],
                 'is_target': i['is_target'],
                 'width': i['width'],
                 'length': i['length']}
            result.append(d)
        return result


x = Chunks()
print(x.__dict__)
