import os
import matplotlib.pyplot as plt
import numpy as np

import config

def save_to_images(x_array, y_array, results_dir, dif):
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    for i in range(len(x_array)):
        label = '_target' if y_array[i] == 1 else '_stray'
        plt.subplot()
        plt.imshow(x_array[i])
        sample_file_name = f'{i + dif}' + label
        plt.savefig(results_dir + sample_file_name)


if __name__ == '__main__':
    dif = 150
    if config.path_to_datasets == '':
        print('Введите путь до npz: ')
        name_of_dir = str(input()) + '/'
    data = np.load('200_test.npz')
    x_train, y_train = data['X_train'], data['y_train']
    x_train = x_train[dif:dif+50]
    y_train = y_train[dif:dif+50]
    most_dir = os.path.dirname(__file__)
    # print('Введите название папки для x_test, y_test: ')
    # name_of_dir = str(input()) + '/'
    # images_here = os.path.join(most_dir, name_of_dir)
    #
    # save_to_images(x_test, y_test, images_here)

    # print('Введите название папки для x_train, y_train: ')
    # name_of_dir = str(input()) + '/'
    name_of_dir = '200_test/'
    images_here = os.path.join(most_dir, name_of_dir)
    save_to_images(x_train, y_train, images_here, dif=dif)