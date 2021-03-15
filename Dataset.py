import numpy as np

from Chunks import Chunks
import input_helper


class Dataset:
    name: str

    # _targets: str  # path to npy with targets
    # _strays: str  # -/\/-
    # _train: str
    # _test: str

    _main: str  # npz

    def __init__(self):
        self._load_name()
        self._load_targets()

    def _load_name(self):
        print('Введите имя для сборки: ')
        self.name = 'dataset_' + str(input())


    def _load_targets(self):
        targets = None
        most_count_of_chunks = 0
        while True:
            yn = {'1': 'Да', '2': 'Нет'}
            print(f'Всего снимков целей в сборке - {most_count_of_chunks}. Добавить?')
            for key in yn:
                print(f'{key} --> {yn[key]}')
            inp = input()
            if inp == '1':
                path_to_bunch_of_chunks, current_count = \
                    Dataset.__one_bunch_of_chunks()
                most_count_of_chunks += current_count
                if targets is None:
                    targets = np.load(path_to_bunch_of_chunks)
                else:
                    targets = np.concatenate((targets, np.load(path_to_bunch_of_chunks)))
            elif inp == '2':





    @staticmethod
    def __one_bunch_of_chunks():
        yn = {'1': 'Да', '2': 'Нет (Создать новую)'}
        print('Загрузить связку снимков из БД?')
        for key in yn:
            print(f'{key} --> {yn[key]}')
        if input() == '1':
            db_chunks = Chunks.fetch_db_chunks()
            value_of_chunks_path, count_of_chunk_in_bunch = \
                input_helper.ForDatasets.choose_chunks_from_list(db_chunks)
        else:
            new_chunks = Chunks()
            value_of_chunks_path = new_chunks.value_path
            count_of_chunk_in_bunch = new_chunks.count
        return value_of_chunks_path, count_of_chunk_in_bunch

if __name__ == '__main__':
    x = Dataset()
