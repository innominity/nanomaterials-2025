import os
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DOCS_DOMAIN_PATH = os.path.join(BASE_DIR, 'data', 'docs', 'domain.xlsx')
DOCS_PHYLUM_PATH = os.path.join(BASE_DIR, 'data', 'docs', 'phylum.xlsx')
DOCS_CLASS_PATH = os.path.join(BASE_DIR, 'data', 'docs', 'class.xlsx')
DOCS_ORDER_PATH = os.path.join(BASE_DIR, 'data', 'docs', 'order.xlsx')
DOCS_FAMILY_PATH = os.path.join(BASE_DIR, 'data', 'docs', 'family.xlsx')
DOCS_SPECIES_PATH = os.path.join(BASE_DIR, 'data', 'docs', 'species.xlsx')

DOCS_FULL_PATH = os.path.join(BASE_DIR, 'data', 'docs', 'full.xlsx')


df_domain = pd.read_excel(DOCS_DOMAIN_PATH)
df_phylum = pd.read_excel(DOCS_PHYLUM_PATH)
df_class = pd.read_excel(DOCS_CLASS_PATH)
df_order = pd.read_excel(DOCS_ORDER_PATH)
df_family = pd.read_excel(DOCS_FAMILY_PATH)
df_species = pd.read_excel(DOCS_SPECIES_PATH)


if __name__ == "__main__":
    print('Генерация полного справочника...')

    print('1/5 - Соединяем `species` <- `family`')
    df_docs = df_species.copy()
    df_merge = df_docs.rename(columns={'name': 'species'}).merge(df_family.rename(columns={'name': 'family', 'id': 'id_family'}), on=['id_family'], how='left')
    
    print('2/5 - Соединяем `family` <- `order`')
    df_merge_2 = df_merge.merge(df_order.rename(columns={'name': 'order', 'id': 'id_order'}), on=['id_order'], how='left')

    print('3/5 - Соединяем `order` <- `class`')
    df_merge_3 = df_merge_2.merge(df_class.rename(columns={'name': 'class', 'id': 'id_class'}), on=['id_class'], how='left')

    print('4/5 - Соединяем `class` <- `phylum`')
    df_merge_4 = df_merge_3.merge(df_phylum.rename(columns={'name': 'phylum', 'id': 'id_phylum'}), on=['id_phylum'], how='left')

    print('5/5 - Соединяем `phylum` <- `domain`')
    df_merge_5 = df_merge_4.merge(df_domain.rename(columns={'name': 'domain', 'id': 'id_domain'}), on=['id_domain'], how='left')

    if len(df_merge_5.isna().sum()[lambda x: x> 0]) != 0:
        print('Ошибка создания файла, сть пропуски при соединении справочников!!!')
        exit()
    
    df_docs_full = df_merge_5[['id', 'species', 'id_family', 'family', 'id_order', 'order', 'id_class', 'class', 'id_phylum', 'phylum', 'id_domain', 'domain']]
    df_docs_full = df_docs_full.rename(columns={'id': 'id_species'})
    df_docs_full.to_excel(DOCS_FULL_PATH, index=False)
    print(r'Создание полного справочника успешно завершено (файл `\data\docs\full.xlsx`)!')

    


