import pathlib
import pandas as pd
import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def primary_analyzer(path: str, sh_name=None, additional_args=None, start=None, stop=None, step=None, out_file=None,
                     directory_name=None, head_or_tail=None, H_T_value=0  ):
    """
    Пишу на русском т.к. это личный проект в первой итерации
    :param path:  определяет путь к вашему excel/csv файлу
    :param sh_name: ОБЯЗАТЕЛЕН, чтобы прочитать excel,xsl,xslx
    :param additional_args:  определяет дополнительные параметры прочитки DataFrame, пишутся как исполняемый код
    Пример: additional_args= "sep=',', usecols=['foo', 'bar', 'baz'] ..."
    :param start: начальный индекс для slice
    :param stop: конечный индекс для slice
    :param step: шаг для slice
    :param out_file: название, общкк, для выходящих файлов, используется для идентификации среди  выходящих файлов
    :param directory_name: директория, куда будут записываться выходящие файлы
    :param head_or_tail: в зависимости 'HEAD'/'TAIL' использует head или  tail к объекту
    :param H_T_value: значение для head/tail
    :return:
    DataFrame формуруeтся следующим образом:
    1)  df=pd.read_...
    2) df=df[start:stop:step]
    3) df=df.head(head_or_tail)/tail(head_or_tail)

    Выходящие файлы:

    1)not_cleahed_data_{out_file}.csv- файл полученный, после формирования

    2)without_NULL_data_{out_file}.csv - файл без строк с NULL

    3)without_NULL_and_0_data_{out_file}.csv- файл без строк с NULL, 0

    4)info_{out_file}.txt- информация о фрейме( df.info, df.columns, df.shape,
    все decsribe для колонок (включены типы ['object', 'str', 'bool']))

    5){column} _info_{out_file}.txt-
    """
    # Чтение и формировка df
    # __________________________________________________________________________________________________________________
    if sh_name:
        if additional_args != None:
            df = eval(f"pd.read_excel('{path}',sheet_name='{sh_name}',{additional_args} )")
        else:
            df = pd.read_excel(path, sheet_name=sh_name)
        df = df[start:stop:step]
        if head_or_tail == 'HEAD':
            df = df.head(H_T_value)
        elif head_or_tail == 'TAIL':
            df = df.tail(H_T_value)
    else:
        if additional_args != None:
            df = eval(f"pd.read_csv('{path}',{additional_args} )")
        else:
            df = pd.read_csv(path)

        df = df[start:stop:step]
        if head_or_tail == 'HEAD':
            df = df.head(H_T_value)
        elif head_or_tail == 'TAIL':
            df = df.tail(H_T_value)
    # __________________________________________________________________________________________________________________

    # Определение общего названия и директории выгрузки
    # __________________________________________________________________________________________________________________
    if out_file == None:
        out_file = generate_random_string(15)

    if directory_name == None:
        directory_name = out_file

    fdir = (pathlib.Path(f'{directory_name}'))
    fdir.mkdir(parents=True, exist_ok=True)
    # __________________________________________________________________________________________________________________

    # Создание файла с выборкой
    # __________________________________________________________________________________________________________________
    file = fdir / f'not_cleahed_data_{out_file}.csv'
    df.to_csv(file)
    # __________________________________________________________________________________________________________________

    # Создание файла без NULL
    # __________________________________________________________________________________________________________________
    filter_cols = ''
    for i in df.columns:
        filter_cols += f"~(df['{i}'].isnull() ) & "

    file = fdir / f'without_NULL_data_{out_file}.csv'
    df.loc[(eval(filter_cols[:-2:]))].to_csv(file)
    # __________________________________________________________________________________________________________________

    # Создание файла без NULL и 0
    # __________________________________________________________________________________________________________________
    for i in df.columns:
        filter_cols += f"(df['{i}'] !=0) & "

    file = fdir / f'without_NULL_and_0_data_{out_file}.csv'
    df.loc[(eval(filter_cols[:-2:]))].to_csv(file)
    # __________________________________________________________________________________________________________________

    # Создание общей сводки
    # __________________________________________________________________________________________________________________
    file = fdir / f'info_{out_file}.txt'

    with open(file, 'w') as f:
        df.info(buf=f)
        info = '\n' + str(df.columns) + '\n' + str(df.shape) + '\n'
        for i in df.columns:
            info += str(df[f"{i}"].describe(include=['object', 'str', 'bool'])) + '\n'
        print(info, file=f)
    # __________________________________________________________________________________________________________________

    #  Создание сводки по колонкам
    # __________________________________________________________________________________________________________________
    for i in df.columns:
        file = fdir / f'{i} _info_{out_file}.txt'
        with open(file, 'w') as f:
            info = ''
            info += str(df[f"{i}"].describe(include=['object', 'str', 'bool'])) + '\n'
            try:
                info += 'Среднее по палате: ' + '\n' + str(df[f"{i}"].mean(numeric_only=True)) + '\n'
            except:
                pass
            info += 'Кол-во нахожденний: ' + '\n' + str(df[f"{i}"].value_counts()) + '\n'
            info += 'Отношение нахожденний к столбцу: ' + '\n' + str(df[f"{i}"].value_counts(normalize=True)) + '\n'
            print(info, file=f)
    # __________________________________________________________________________________________________________________


primary_analyzer(path='kc_house_data.csv', out_file='csv_file', additional_args='sep=","')

primary_analyzer(path='OOO_Vnimanie_k_detalyam_2__1.xlsx', directory_name='excel_file', sh_name='Справочник точек',
                 stop=150, head_or_tail='TAIL', H_T_value=-100)
