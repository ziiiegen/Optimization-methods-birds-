"""
Скрипт загружает данные из файла обрабатывает их и проверяет на удовлетворение условий проекту.
Также создает класс для каждого файла отдельно, загружая в него характеристи файла и результаты проверки.
"""

import os
import pandas as pd
import io
import sys

class Birds():
    def __init__(self, file_name):
        self.file_name = file_name

def prepare_data(data_birds):
    """ 
    Функция обрабатывыет входной файл с птицами
    data - все ветки с птицами без пробелов
    set_birds_data - уникальные птицы
    """
    data = data_birds[5:-3]

    set_birds_data = {x for x in set(data) if x.isalpha()}

    for i in range(len(data)-1, 0, -1):
        if data[i] in set_birds_data:
            data = data[:i+1]
            break

    return data.replace(" ", ""), set_birds_data

def count_branch_in_file(file_birds, data_birds, prepared_arr_birds):
    """
    Функция для подсчета веток с помощью вхождения \n 
    """
    count_string_file = data_birds.count('\n')
    count_string_prepare_arr = prepared_arr_birds.count('\n')

    file_birds.count_branch = count_string_file - 2
    file_birds.count_full_branch = count_string_prepare_arr + 1
    file_birds.count_empty_branch = count_string_file - count_string_prepare_arr - 3

def check_count_birds_on_branch(prepared_arr_birds):
    """
    Функция проверяет, что каждая ветка с птицами полностью заполнена.
    Возвращает результат проверки и длину ветки (колличество птиц на ветке).
    """
    len_first_string = prepared_arr_birds.find('\n')

    count_symbol_in_string = 0
    # flag = True
    flag = [True, 0]

    for bird in prepared_arr_birds:
        if (bird == '\n') and (len_first_string != count_symbol_in_string):
            flag = [False, None]
            break
        elif (bird == '\n') and (len_first_string == count_symbol_in_string):
            flag = [True, count_symbol_in_string]
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

def check_miltiplicity_birds_of_branch(file_birds):
    """
    Функция проверяет кратность количества птиц размеру ветки
    """
    if (file_birds.birds_on_branch[0] == False):
        return [False, None]
    
    for key, value in file_birds.dict_birds.items():
        if value % file_birds.birds_on_branch[1] != 0:
            result = [False, key]
            return result
    return [True]

def print_summary(file_birds):
    """
    Функция выводит результаты
    """    
    print("=" * 50)
    print(f"""
    Проверка файла: {file_birds.file_name[1:]}
    Количество веток: {file_birds.count_branch}
    Количество заполненных веток: {file_birds.count_full_branch}
    Количество пустых веток: {file_birds.count_empty_branch}
    """)
    print("-" * 30)

    df = pd.DataFrame(list(file_birds.dict_birds.items()), columns=['Птица', 'Количество'])
    print(df)

    print("-" * 30)
    print(f"""
    Длина заполненных веток: {file_birds.birds_on_branch}
    Кратность птиц одного типа: {file_birds.miltiplicity_birds}
    """)
    print("=" * 50)

def check_file(input_file, save=True):
    current_dir = os.path.dirname(__file__)
    input_dir = os.path.join(current_dir, '..', '..', 'data', 'input')
    output_dir=os.path.join(current_dir,'..','..','data','output')
    os.makedirs(output_dir,exist_ok=True)

    report_path=os.path.join(output_dir,"report.txt")
    for file in input_file:
        file_birds = Birds(file)

        with open(input_dir+file, "r") as f:
            data_birds = f.read()
        
        prepared_arr_birds, set_birds_data = prepare_data(data_birds)

        count_branch_in_file(file_birds, data_birds, prepared_arr_birds)

        result_branch = check_count_birds_on_branch(prepared_arr_birds)
        file_birds.birds_on_branch = result_branch

        dict_birds = creation_dictionary_birds(prepared_arr_birds, set_birds_data)
        file_birds.dict_birds = dict_birds

        result_birds = check_miltiplicity_birds_of_branch(file_birds)
        file_birds.miltiplicity_birds = result_birds

        if save:

            buffer=io.StringIO()
            old_stdout=sys.stdout
            sys.stdout=buffer

            try:
                print_summary(file_birds)
            finally:
                sys.stdout=old_stdout

            with open(report_path,"a",encoding="utf-8") as f:
                f.write(buffer.getvalue())

        else:
            print_summary(file_birds)

if __name__ == '__main__':
    INPUT_FILE = ["/BIRDS_3.txt", "/BIRDS_4.txt", "/BIRDS_5.txt", "/BIRDS_6.txt",
                  "/BIRDS_7.txt", "/BIRDS_8.txt", "/BIRDS_9.txt", "/BIRDS_10.txt",
                  "/BIRDS_11.txt", "/BIRDS_12.txt", "/BIRDS_13.txt"]
    check_file(INPUT_FILE)
    
