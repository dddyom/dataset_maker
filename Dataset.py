import numpy as np
from typing import List
from Chunks import Chunks


class Dataset:
    name: str
    # _chunks: List[Chunks]
    #
    # _targets: str  # path to npy with targets
    # _strays: str  # -/\/-
    # _train: str
    # _test: str

    _main: str  # npz

    def __init__(self):
        self._load_name()

    def _load_name(self):
        self.name = 'dataset_' + str(input())

    def _load_targets(self):
        yn = {'1': 'Да', '2': 'Нет (Создать новую)'}
        print('Загрузить связку снимков из БД?')
        for key in yn:
            print(f'{key} --> {yn[key]}')
        if input() == '1':
            db_chunks = Chunks.fetch_db_chunks()
            self._motherMatrixPath, self._motherMatrixName, self._coordinates = \
                input_helper.ForChunks.choise_matrix_from_list(db_chunks)