from Matrix import Matrix
from Chunks import Chunks
from Dataset import Dataset

if __name__ == '__main__':
    yn = {'1': 'Создать матрицу',
          '2': 'Создать связку снимков',
          '3': 'Создать сборку'}
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
        else:
            print('Некорректный ввод')