import os
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_PATH_PREPARE = os.path.join(BASE_DIR, 'data', 'prepare', 'data.xlsx')
DOCS_SPECIES_PATH = os.path.join(BASE_DIR, 'data', 'docs', 'species.xlsx')

DATA_PATH_CLEAN = os.path.join(BASE_DIR, 'data', 'clean', 'data.xlsx')
DATA_UNWRAP_PATH_CLEAN = os.path.join(BASE_DIR, 'data', 'clean', 'data_unwrap.xlsx')

def make_transpose_by_col(df: pd.DataFrame, ind_cols, feature_col: list, feature_col_available: str, col_values: str) -> pd.DataFrame:
    """
    Разорачивание DataFrame по столбцу с индексами и признаками

    Args:
        df (pd.DataFrame): исходный датафрейм
        ind_cols (list): список столбцов в котором индекс (по каким столбцам разворачивать)
        feature_col (str): столбец признак
        feature_col_available (list): список допустимых значений по столбцу
        col_values (str): столбец значение
    """

    df_index = df[ind_cols].drop_duplicates().reset_index(drop=True)
    df_result_list = []
    for _, row in df_index.iterrows():
        df_result_iter = []
        df_filter = df
        for col in ind_cols:
            df_filter = df_filter[df_filter[col] == row[col]]
            df_result_iter.append(row[col])
        df_filter = df_filter[[feature_col, col_values]]
        for col in feature_col_available:
            df_filter_col = df_filter[df_filter[feature_col] == col].reset_index(drop=True)
            if len(df_filter_col) != 1:
                df_result_iter.append(np.nan)
            else:
                df_result_iter.append(df_filter_col.loc[0, col_values])
        df_result_list.append(df_result_iter)

    df_columns_names = ind_cols + feature_col_available
    return pd.DataFrame(df_result_list, columns=df_columns_names)



if __name__ == "__main__":
    print('Создание чистых данных для анализа...')
    df_prepare = pd.read_excel(DATA_PATH_PREPARE)
    df_species = pd.read_excel(DOCS_SPECIES_PATH)

    LIST_FEATURES = list(df_species['name'].values)

    df_prepare_transpose = make_transpose_by_col(df_prepare, ['target', 'group'], 'type_of_bacterium', LIST_FEATURES, 'count')
    
    # Удаляем ненужный target
    print('Удаление строк с "target" = 9495')
    df_prepare = df_prepare[df_prepare['target'] != 9495]
    df_prepare_transpose = df_prepare_transpose[df_prepare_transpose['target'] != 9495]

    # удаляем группу так как это просто номер курицы бройлера
    print('Переименование старой колонки "group" -> "number"')
    df_prepare_transpose = df_prepare_transpose.rename(columns={'group': 'number'})
    df_prepare = df_prepare.rename(columns={'group': 'number'})

    # Заменяем в развернутом наборе данных строку с 
    df_prepare = df_prepare.rename(columns={'type_of_bacterium': 'species'})
    df_prepare_docs = df_prepare.merge(df_species.rename(columns={'name': 'species', 'id': 'id_species'}), on=['species'], how='left')
    df_prepare = df_prepare_docs[['target', 'number', 'id_species', 'count']]

    print('Приводим в нужную стрктуру target -> group, count -> colonies')
    df_prepare = df_prepare.rename(columns={'target': 'group', 'count': 'colonies'})
    df_prepare_transpose = df_prepare_transpose.rename(columns={'target': 'group', 'count': 'colonies'})

    # Сохраняем обработанные файлы
    df_prepare.to_excel(DATA_UNWRAP_PATH_CLEAN, index=False)
    df_prepare_transpose.to_excel(DATA_PATH_CLEAN, index=False)
    print(r'Создание чистых данных для анализа успешно завершено (каталог `\data\clean`)!')

    


