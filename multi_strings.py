#!/usr/bin/env python3

"""

Программа создана для консультантов IBM Cognos, которым необходимо писать идентичный код процессов и правил кубов
для нескольких элементов.

На вход программа принимает шаблон, вставляемые элементы и базовую строку.
Результатом программы будет вывод измененных строк.

Особенность записи шаблонов и вставляемых элементов:
    Шаблоны и вставляемые элементы для каждой новой строки необходимо перечислять через запятую:
    Если в одгной строке кода используется несколкько шаблонов и элементов, то для одной строки шаблоны и вставляенмые
    элементы разделяются пробелом:

Пример работы программы для 1 шаблона в строке:
Шаблон - ###
Вставляемые элементы - янв, фев, мар
Базовая строка - ['###'] = DB('Расходны на персонал', !Тип данных, !Год, !Версия, !Подразделение, '###')

Выход программы:
['янв'] = DB('Расходны на персонал', !Тип данных, !Год, !Версия, !Подразделение, 'янв')
['фев'] = DB('Расходны на персонал', !Тип данных, !Год, !Версия, !Подразделение, 'фев')
['мар'] = DB('Расходны на персонал', !Тип данных, !Год, !Версия, !Подразделение, 'мар')


Пример работы программы с 2 и более шаблонами в строке:
Шаблон - ##, ^^
Вставляемые элементы - vsPodr Подразделение, vsDir ДиР
Базовая строка - CellPutS(##, 'Сотрудники', !Тип данных, !Год, !Версия, !Должность, '^^')

Выход программы:
CellPutS(vsPodr, 'Сотрудники', !Тип данных, !Год, !Версия, !Должность, 'Подразделение')
CellPutS(vsDir, 'Сотрудники', !Тип данных, !Год, !Версия, !Должность, 'ДиР')

Для удобства данную программу можно вызывать через терминал с использованием параметров:

-h вызов инструкции по работе со скриптом
-f шаблон. По умолчанию шаблоном является ###
-r всавляемые элементы, перечислянные через запятую.

"""
import sys
import os
from datetime import datetime
import log
import logging
import logging.config
from const import *

# настройка логирования
logfile_name = os.path.join(sys.path[0], f"{datetime.now().strftime('%Y%m%d')}.log")
# logfile_name = os.path.join(sys.path[0], f"python.log")
logging.config.fileConfig(fname='log.cnf', defaults={'logfilename': logfile_name}, disable_existing_loggers=False)
# logger1 = logging.getLogger(__name__)
logger = logging.getLogger('progLogger')
# logger.setLevel(logging.INFO)
#
# f_handler = logging.FileHandler(logfile_name)
# f_handler.setLevel(logging.INFO)
#
# f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# f_handler.setFormatter(f_format)
#
# logger.addHandler(f_handler)

# получаем список переданных параметров
arguments = sys.argv[1:]

@log.start_program(logger)
def welcome():
    with open('welcome.txt', 'r') as f:
        welcome_str = f.read()

    return welcome_str


def dub_months(find_value, replace_value):
    """
    Функция берет на вход шаблон и список значений, на которые заменяется шаблон.
    Пользователь вводить строку и далее в цикле происходит замена шаблона на значения из списка.
    Все новые строки выводятся на экран.

    :param find_value: шаблон, string
    :param replace_value: список строковых значений, array
    """

    base_string = input('Введите редактируемую строку:\n')
    if base_string == '':
        base_string = f"['{find_str[0]}'] = DB('Расходны на персонал', !Тип данных, !Год, !Версия, !Подразделение, '{find_str[0]}')"
    new_strings = []
    for value in replace_value:
        new_str = base_string
        for i, rep in enumerate(value.split()):
            new_str = new_str.replace(find_value[i].strip(), rep.strip())
        new_strings.append(new_str)
    return new_strings


if __name__ == '__main__':



    # если параметров нет, значит запущена программа для использования несколько раз
    # и выводится приветствие
    if arguments != ['']:
        print(welcome())

    while True:
        # флаг для выхода из программы
        quit_flag = 0

        # парметр, определяющий шаблон
        if '-f' in arguments:
            f_ind = arguments.index('-f') + 1
            find_str = arguments[f_ind]
            quit_flag = 1
        else:
            find_str = input('Введите шаблон замены:\n').split(',')
            if find_str == ['']:
                print('Автоматически создан шаблон - ###\n')
                find_str = TEMPLATE

        # параметр, определяющий список
        # заначений,на которые заменится шаблон
        if '-r' in arguments:
            r_ind = arguments.index('-r') + 1
            rep_str = arguments[r_ind].split()
            quit_flag = 1
        else:
            rep_str = input('Введите список новых значений:\n').split(',')
            if rep_str == ['']:
                rep_str = REP_DATA


        new_strings = dub_months(find_str, rep_str)
        print(*new_strings, sep='\n')

        # условие выхода из цикла
        if quit_flag == 1:
            sys.exit()

