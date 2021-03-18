
import input_helper

from png_control import npz_to_png
from Matrix import Matrix
from Chunks import Chunks
from Dataset import Dataset

if __name__ == '__main__':
    yn = {'1': 'Создать матрицу',
          '2': 'Создать связку снимков',
          '3': 'Создать сборку',
          '4': 'Склеить сборки (train + test)',
          '5': 'Сохранить в png',
          '6': 'Завершить работу'}
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
            path_to_datasets = input_helper.ForDatasets.get_path_of_dataset()
            dataset = input_helper.ForDatasets.merge_test_and_train(path_to_datasets)
            Dataset.merge_datasets(path_to_datasets + '/' + dataset + '/' + dataset)

        elif inp == '5':
            npz_to_png()

        elif inp == '6':
            break
        else:
            print('Некорректный ввод')
