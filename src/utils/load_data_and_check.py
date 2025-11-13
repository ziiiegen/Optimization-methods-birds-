"""
Функция загружает данные из файла обрабатывает их и проверяет на удовлетворение условий проекту.
Также создает класс для каждого файла отдельно, загружая в него характеристи файла и результаты проверки.
"""

import os

class Birds():
    def __init__(self, file_name):
        self.file_name = file_name

def prepare_data(data_birds):
    """ 
    Функция убирает первую, последнюю строки и пустые ветки, оставляя только полные
    Также делает set из букв
    """
    data = data_birds[5:-3]

    set_birds_data = {x for x in set(data) if x.isalpha()}

    for i in range(len(data)-1, 0, -1):
        if data[i] in set_birds_data:
            data = data[:i+1]
            break

    return data, set_birds_data

def count_branch_in_file(file_birds, data_birds, prepared_arr_birds):
    """
    Функция для подсчета веток с помощью вхождения \n 
    """
    count_string_file = data_birds.count('\n')
    count_string_prepare_arr = prepared_arr_birds.count('\n')
    file_birds.count_branch = count_string_file - 2
    file_birds.count_full_branch = count_string_prepare_arr + 1
    file_birds.count_empty_branch = count_string_file - count_string_prepare_arr - 3

def check_birds_on_branch(prepared_arr_birds, end_string_id, file):
    """
    Функция проверяет, что каждая ветка с птицами полностью заполнена
    """
    count_symbol_in_string = 0
    flag = True

    for bird in prepared_arr_birds:
        if (bird == '\n') and (end_string_id != count_symbol_in_string):
            flag = False
        elif (bird == '\n') and (end_string_id == count_symbol_in_string):
            count_symbol_in_string = 0
        else:
            count_symbol_in_string += 1

    return flag

def creation_dictionary_birds(prepared_arr_birds, set_birds_data):
    """
    Функция создает словарь, где ключ - птица, значение - ее количество на ветках
    """
    dict_birds = {}

    for i in set_birds_data:
        dict_birds[i] = 0
    for i in prepared_arr_birds:
        if i in set_birds_data:
            dict_birds[i] += 1
    
    return dict_birds

def check_miltiplicity_birds_of_branch(dict_birds, end_string_id, file):
    """
    Функция проверяет кратность количества птиц размеру ветки
    """
    count_birds_on_branch = (end_string_id+ 1)/2 
    flag = True
    for key, value in dict_birds.items():
        if value % count_birds_on_branch != 0:
            flag = False
            result = [key, flag]
            return result
    return [flag]

def print_summary(file_birds):
    """
    Функция выводит результаты
    """    
    print(
            f"""

    Проверка файла {file_birds.file_name}
Количество веток: {file_birds.count_branch}
Количество заполненных веток: {file_birds.count_full_branch}
Количество пустых веток: {file_birds.count_empty_branch}

Типы и количество птиц:
{file_birds.dict_birds}

Длина заполненных веток: {file_birds.birds_on_branch}
Кратность птиц одного типа: {file_birds.miltiplicity_birds}

""")

def check_file(input_file, save=False):
    current_dir = os.path.dirname(__file__)
    input_dir = os.path.join(current_dir, '..', '..', 'data', 'input')

    for file in input_file:
        file_birds = Birds(file)

        with open(input_dir+file, "r") as f:
            data_birds = f.read()
        
        prepared_arr_birds, set_birds_data = prepare_data(data_birds)

        count_branch_in_file(file_birds, data_birds, prepared_arr_birds)

        end_string_id = prepared_arr_birds.find('\n')
        file_birds.len_full_branch = int((end_string_id + 1) / 2)

        result_branch = check_birds_on_branch(prepared_arr_birds, end_string_id, file)
        file_birds.birds_on_branch = result_branch

        dict_birds = creation_dictionary_birds(prepared_arr_birds, set_birds_data)
        file_birds.dict_birds = dict_birds

        result_birds = check_miltiplicity_birds_of_branch(dict_birds, end_string_id, file)
        file_birds.miltiplicity_birds = result_birds

        if save:
            pass
        else:
            print_summary(file_birds)


if __name__ == '__main__':
    INPUT_FILE = ["/BIRDS_3.txt", "/BIRDS_4.txt", "/BIRDS_5.txt", "/BIRDS_6.txt",
                  "/BIRDS_7.txt", "/BIRDS_8.txt", "/BIRDS_9.txt", "/BIRDS_10.txt",
                  "/BIRDS_11.txt", "/BIRDS_12.txt", "/BIRDS_13.txt"]
    check_file(INPUT_FILE)
    
