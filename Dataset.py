import numpy as np
from pathlib import Path

from Chunks import Chunks
import input_helper
import config


class Dataset:
    name: str
    dataset_folder: str

    _targets: str  # path to npy with targets
    _strays: str  # -/\/-
    # _train: str
    # _test: str

    _main: str  # npz

    def __init__(self):
        self._load_name()
        self._load_chunks()
        self._load_chunks(strays=True)

    def _load_name(self):
        print('Введите имя для сборки: ')
        self.name = 'dataset_' + str(input())

    def _load_chunks(self, strays=False):
        chunks = None
        most_count_of_chunks = 0
        yn = {'1': 'Да', '2': 'Нет'}
        label = 'ПОМЕХ' if strays else 'ЦЕЛЕЙ'
        print(f'ДОБАВЛЕНИЕ {label}')

        while True:

            print(f'Всего снимков {label} в сборке - {most_count_of_chunks}. Добавить?')
            for key in yn:
                print(f'{key} --> {yn[key]}')
            inp = input()
            if inp == '1':
                path_to_bunch_of_chunks, current_count = \
                    Dataset.__one_bunch_of_chunks()
                most_count_of_chunks += current_count
                if chunks is None:
                    chunks = np.load(path_to_bunch_of_chunks)
                else:
                    chunks = np.vstack((chunks, np.load(path_to_bunch_of_chunks)))
            elif inp == '2':
                Dataset.__save_path(self)
                if strays:
                    np.save(self._strays, chunks)
                    return
                np.save(self._targets, chunks)
                break
            else:
                print('Введите 1 для добавления новых снимков или 2 для завершения')

    def __save_path(self):
        if config.path_to_datasets == '':
            path_to_datasets = input_helper.get_path()
        else:
            path_to_datasets = config.path_to_datasets
        self.dataset_folder = path_to_datasets + '/' + self.name
        Path(self.dataset_folder).mkdir(parents=True, exist_ok=True)
        self._targets = self.dataset_folder + '/targets.npy'
        self._strays = self.dataset_folder + '/strays.npy'

    @staticmethod
    def __one_bunch_of_chunks():
        yn = {'1': 'Да', '2': 'Нет (Создать новую)'}
        while True:
            print('Загрузить связку снимков из БД?')
            for key in yn:
                print(f'{key} --> {yn[key]}')
            if input() == '1':
                db_chunks = Chunks.fetch_db_chunks()
                if not db_chunks:
                    print('БД пуста. Создайте значения')
                    continue
                value_of_chunks_path, count_of_chunk_in_bunch = \
                    input_helper.ForDatasets.choose_chunks_from_list(db_chunks)
            else:
                new_chunks = Chunks()
                value_of_chunks_path = new_chunks.value_path
                count_of_chunk_in_bunch = new_chunks.count
            return value_of_chunks_path, count_of_chunk_in_bunch


if __name__ == '__main__':
    x = Dataset()
