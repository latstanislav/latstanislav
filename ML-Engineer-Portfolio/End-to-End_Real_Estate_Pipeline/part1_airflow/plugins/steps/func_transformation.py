import pandas as pd


def remove_duplicates(data: pd.DataFrame):
    feature_cols = [col for col in data.columns if col != 'id']
    is_duplicated_features = data.duplicated(subset=feature_cols, keep=False)
    data = data[~is_duplicated_features].reset_index(drop=True)
    return data 

def remove_outliers(data: pd.DataFrame):
    num_cols = ['total_area','price','flats_count']
    threshold = 1.5
    potential_outliers = pd.DataFrame()

    for col in num_cols:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        margin = threshold*IQR 
        lower = Q1 - margin 
        upper = Q3 + margin 
        potential_outliers[col] = ~data[col].between(lower, upper)

    outliers = potential_outliers.any(axis=1)
    data=data[~outliers].reset_index(drop=True)

    return data

def remove_none(data: pd.DataFrame):
    '''
    Изучив таблицу, кажется допустимым заполнять пустые ячейки наиболее частым значением,
    но если потребуется улучшить точность модели и в случае наличия большого количества пропусков, 
    можно пройтись по каждому столбцу и подумать
    '''
    cols_with_nans = (data.isnull() | (data=='')).sum()
    cols_with_nans = cols_with_nans[cols_with_nans > 0].index

    for col in cols_with_nans:
        fill_value = data[col].mode().iloc[0]
        data[col] = data[col].fillna(fill_value)
    return data