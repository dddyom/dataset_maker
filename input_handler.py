import glob
from exceptions import InputError


def input_handler_for_label(query_label):
    """Запрашивает тип кэша"""
    def input_result_wrapper(self, label):
        caches_dict = {'1': 'BI', '2': 'SO', '3': 'SN', '4': 'SI'}
        print('\nТип кэша: (ожидается индекс)')
        while True:
            for key in caches_dict:
                print(f'{key} --> {caches_dict[key]}')
            try:
                label = caches_dict[str(input())]
            except (UnboundLocalError, KeyError) as e:
                print(e, 'Ожидается индекс')
                continue
            break
        query_label(self, label)
    return input_result_wrapper



# @input_handler_for_label
# def decorated_function_with_arguments(function_arg1):
#     print(function_arg1)


# decorated_function_with_arguments()

# def input_handler(type_of_input):
#     def expected_input_handler(get_attribute_value):
#         """Запрашивает тип кэша"""
#         caches_dict = {'1': 'BI', '2': 'SO', '3': 'SN', '4': 'SI'}
#         print('\nТип кэша: (ожидается индекс)')
#         while True:
#             for key in caches_dict:
#                 print(f'{key} --> {caches_dict[key]}')
#             try:
#                 label = caches_dict[str(input())]
#             except (UnboundLocalError, KeyError) as e:
#                 print(e, 'Ожидается индекс')
#                 continue
#             break
#         caches_dict.get(type_of_input)
#         def input_result_handler():
#             return get_attribute_value(label)
#         return input_result_handler
#     return expected_input_handler



# while True:
#     label = 'SO'
#     print(f'Путь до {label} кэша:')
#     path = str(input()) + f'/{label}*'
#     try:
#         list_of_caches = glob.glob(path)
#         if not list_of_caches:
#             raise InputError('Некорректный путь --> ', path)
#         print(list_of_caches)
#         break
#     except InputError as e:
#         print(e.args)
