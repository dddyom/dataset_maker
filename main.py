import os

import config
import input_helper
from Matrix import Matrix
from Chunks import Chunks
from Dataset import Dataset

if __name__ == '__main__':
    yn = {'1': 'Создать матрицу',
          '2': 'Создать связку снимков',
          '3': 'Создать сборку',
          '4': 'Склеить сборки (train + test)',
          '5': 'Завершить работу'}
    while True:
        for key in yn:
            print(f'{key} --> {yn[key]}')
        inp = input()
        if inp == '1':
            x = Matrix()
        elif inp == '2':
            x = Chunks()
        elif inp == '3':
            x = Dataset()
        elif inp == '4':
            if config.path_to_datasets == '':
                path_to_datasets = input_helper.get_path()
            else:
                path_to_datasets = config.path_to_datasets
            list_with_datasets = os.listdir(path_to_datasets)
            while True:
                print('Имя кэша с матрицей (индекс): ')
                for index, name in enumerate(list_with_datasets):
                    print(index, ' --> ', name)
                try:
                    dataset = list_with_datasets[int(input())]
                    Dataset.merge_datasets(path_to_datasets + '/' + dataset + '/'+ dataset)
                    break
                except (IndexError, TypeError, ValueError) as e:
                    print(f'Ожидается индекс от 0 до {len(list_with_datasets) - 1}')
        elif inp == '5':
            break
        else:
            print('Некорректный ввод')
