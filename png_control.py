import os
import pathlib
import re
import shutil
from typing import List

import matplotlib.pyplot as plt
import numpy as np

import config
import input_helper


def move_dir(src: str, dst: str, pattern: str = '*'):
    if not os.path.isdir(dst):
        pathlib.Path(dst).mkdir(parents=True, exist_ok=True)
    for f in os.listdir(src):
        if pattern in f:
            shutil.move(os.path.join(src, f), os.path.join(dst, f))


def save_to_images(x_array, y_array, results_dir, dif) -> None:
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    for i in range(len(x_array)):
        label = '_target' if y_array[i] == 1 else '_stray'
        plt.subplot()
        plt.imshow(x_array[i])
        sample_file_name = f'{i + dif}' + label
        plt.savefig(results_dir + sample_file_name)


def get_list_of_npz_arrays(path_to_files) -> List:
    list_of_npz_arrays = []
    list_of_dataset_files = os.listdir(path_to_files)
    for i in list_of_dataset_files:
        temp = re.findall('npz', i)
        if temp:
            list_of_npz_arrays.append(i)
    if not list_of_npz_arrays:
        print('Отсутствуют файлы в формате npz')
    return list_of_npz_arrays


def save_png_by_path(most_path, npz_array) -> None:
    data = np.load(most_path + npz_array)
    while True:
        try:
            x, y = data['x'], data['y']
            name_of_dir_png = f'{npz_array[:-4]}_png/'
            png_save_here = most_path + name_of_dir_png
            save_to_images(x, y, png_save_here, 0)
            sort_by_folders(png_save_here)
        except KeyError:
            print("Ожидается сборка train или test, не main. В npz архиве не найден массив по ключу 'x'")
        finally:
            return


def get_npz_array_from_list(list_of_npz_arrays) -> str:
    while True:
        print('Имя сборки (индекс): ')
        for index, value in enumerate(list_of_npz_arrays):
            print(index, ' --> ', value)
        try:
            npz_array = list_of_npz_arrays[int(input())]
            return npz_array
        except (IndexError, TypeError, ValueError):
            print(f'Ожидается индекс от 0 до {len(list_of_npz_arrays) - 1}')


def get_dataset_path(path_to_all_datasets) -> List:
    list_with_datasets = os.listdir(path_to_all_datasets)
    while True:
        print('Имя сборки (индекс): ')
        for index, name in enumerate(list_with_datasets):
            print(index, ' --> ', name)
        try:
            dataset = list_with_datasets[int(input())]
            path_to_files = path_to_all_datasets + f'/{dataset}/'
            return path_to_files
        except (IndexError, TypeError, ValueError):
            print(f'Ожидается индекс от 0 до {len(list_with_datasets) - 1}')


def npz_to_png() -> None:
    if config.path_to_datasets == '':
        path_to_datasets = input_helper.get_path()
    else:
        path_to_datasets = config.path_to_datasets
    path_to_dataset_files = get_dataset_path(path_to_datasets)
    list_of_npz = get_list_of_npz_arrays(path_to_dataset_files)
    npz_name = get_npz_array_from_list(list_of_npz)
    save_png_by_path(path_to_dataset_files, npz_name)


def sort_by_folders(source):
    dst1 = os.path.normpath(source + '/targets/')
    dst2 = os.path.normpath(source + '/strays/')
    move_dir(source, dst1, pattern='_target.png')
    move_dir(source, dst2, pattern='_stray.png')


if __name__ == '__main__':
    npz_to_png()
