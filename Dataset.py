import numpy as np
from pathlib import Path

from sklearn.utils import shuffle
# from sklearn.model_selection import train_test_split

from Chunks import Chunks
import input_helper
import config
import db


class Dataset:
    name: str
    dataset_folder: str

    _targets: str  # path to npy with targets
    _strays: str  # -/\/-

    _train: str
    _test: str

    def __init__(self):
        self._load_name()
        self._load_chunks()
        self._load_chunks(strays=True)

        self._init_train_and_test()
        db.insert('datasets', {'name': self.name,
                               'dataset_folder': self.dataset_folder,
                               'targets': self._targets,
                               'strays': self._strays,
                               })

    def _load_name(self):
        print('Введите имя для сборки: ')
        self.name = 'dataset_' + str(input())

    def _load_chunks(self, strays=False):
        if strays:
            try:
                chunks = np.load(self._strays)
                most_count_of_chunks = len(chunks)
            except Exception:
                chunks = None
                most_count_of_chunks = 0
            label = 'ПОМЕХ'
        else:
            try:
                chunks = np.load(self._targets)
                most_count_of_chunks = len(chunks)
            except Exception:
                chunks = None
                most_count_of_chunks = 0
            label = 'ЦЕЛЕЙ'

        yn = {'1': 'Да', '2': 'Нет'}
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

    def _init_train_and_test(self):
        yn = {'1': 'train', '2': 'test'}

        targets, target_labels = self.__get_labels()
        strays, stray_labels = self.__get_labels(strays=True)
        while True:
            print('Выберите тип ')
            for key in yn:
                print(f'{key} --> {yn[key]}')
            inp = input()
            if inp != '1' and inp != '2':
                print('Введите 1 или 2 для выбора типа сборки')
                continue
            print(f'''Сборка {yn[inp]}:\nКоличество целей -->{len(targets)}\nКоличество помех -->{len(strays)}
                      ''')
            x = np.vstack((targets, strays))
            y = np.concatenate((target_labels, stray_labels))
            x, y = shuffle(x, y, random_state=0)
            np.savez_compressed(f'{self.dataset_folder}/{self.name}_{yn[inp]}.npz', x=x, y=y)
            return

    def __get_labels(self, strays=False):
        arr = np.load(self._strays) if strays else np.load(self._targets)
        labels = np.ones(len(arr)) if not strays else np.zeros(len(arr))
        return arr, labels

    @staticmethod
    def merge_datasets(path):
        try:
            npz_train = np.load(path + '_train.npz')
            npz_test = np.load(path + '_test.npz')
            x_train, y_train = npz_train['x'], npz_train['y']
            x_test, y_test = npz_test['x'], npz_test['y']
            np.savez_compressed(f'{path}_main.npz', x_train=x_train, x_test=x_test,
                                y_train=y_train, y_test=y_test)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    x = Dataset()
