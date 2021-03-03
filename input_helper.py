from typing import List
import glob
import os

class ForMatrixes:
    @staticmethod
    def set_label_of_cache():
        caches_dict = {'1': 'BI', '2': 'SO', '3': 'SN', '4': 'SI'}
        print('\nТип кэша: (ожидается индекс)')
        while True:
            for key in caches_dict:
                print(f'{key} --> {caches_dict[key]}')
            try:
                label = caches_dict[str(input())]
                return label
            except (UnboundLocalError, KeyError) as e:
                print(e, 'Ожидается индекс')

    @staticmethod
    def set_path_of_cache(label):
        while True:
            print(f'Путь до {label} кэша:')
            path = str(input())
            temp = path + f'/{label}*'
            try:
                list_of_caches = glob.glob(temp)
                if not list_of_caches:
                    raise ValueError
                return path
            except ValueError as e:
                print(f'''Некорректный путь (Либо в папке отсутствует
                кэш в формате {label}*.txt)-->''', temp)

    @staticmethod
    def set_name_of_cache(path):
        list_with_caches = os.listdir(path)
        while True:
            print('Имя кэша с матрицей (индекс): ')
            for index, name in enumerate(list_with_caches):
                print(index, ' --> ', name)
            try:
                name = list_with_caches[int(input())]
                return name[:-4]
            except (IndexError, TypeError, ValueError) as e:
                print(f'Ожидается индекс от 0 до {len(list_with_caches)}')

    @staticmethod
    def get_coordinates_for_cache(name) -> List:
        result = []
        while True:
            print(f"Азимут, дальность для цели"
                f"\n{name} "
                "\nкэша в формате:"
                "\nA1 D1"
                "\nA2 D2")
            all_coordinates_in_str = list(iter(input, ''))
            for one_line_with_coordinates in all_coordinates_in_str:
                one_line_with_coordinates = one_line_with_coordinates.split()
                try:
                    if len(one_line_with_coordinates) > 2:
                        raise ValueError('Неверное количество аргументов -->', one_line_with_coordinates)
                    result.append(list(map(int, one_line_with_coordinates)))
                except (ValueError, TypeError) as e:
                    print(e)
                    continue
                return result

    @staticmethod
    def get_path_for_npy():
        while True:
            print('Путь для сохранения матрицы в npy: ')
            path = str(input())
            try:
                if not os.path.isdir(path):
                    raise ValueError
                return path
            except ValueError as e:
                print('Некорректный путь -->', path)
                continue


class ForChunks:
    @staticmethod
    def choise_matrix_from_list(list_of_matrixes):
        while True:
            for index, value in enumerate(list_of_matrixes):
                print(f'{index} --> {value}')
                try:
                    ind = int(input())
                    name = list_of_matrixes[ind]['name']
                    coordinates = list_of_matrixes[ind]['coordinates']
                    return name, coordinates
                except (IndexError, TypeError, ValueError) as e:
                    print(f'Ожидается индекс от 0 до {len(list_of_matrixes)}')

    @staticmethod
    def set_dimensions_of_chunk():
        while True:
            print('Введите ширину: ')
            try:
                width = int(input())
                break
            except (TypeError, ValueError) as e:
                print('Неверно введены данные, попробуйте ещё раз: ')
        while True:
            print('Введите длину: ')
            try:
                lengtn = int(input())
                return width, lengtn
            except (TypeError, ValueError) as e:
                print('Неверно введены данные, попробуйте ещё раз: ')

    @staticmethod
    def set_type_of_chunk():
                yn = {'1': 'Цели', '2': 'Помехи'}
                while True:
                    print('''Тип снимков
                    \nОжидается 1 для целей или 2 для помех''')
                    for key in yn:
                        print(f'{key} --> {yn[key]}')
                    ind = input()
                    if  ind == '1':
                        return True
                    elif ind == '2':
                        return False
