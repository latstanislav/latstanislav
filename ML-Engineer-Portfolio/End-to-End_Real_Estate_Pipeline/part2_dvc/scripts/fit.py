import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from category_encoders import CatBoostEncoder
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from catboost import CatBoostRegressor
import yaml
import os
import joblib


# обучение модели
def fit_model():
	# Прочитайте файл с гиперпараметрами params.yaml
    with open('params.yaml', 'r') as fd:
        params = yaml.safe_load(fd)
    # загрузите результат предыдущего шага: inital_data.csv
    data = pd.read_csv('data/dvc_data.csv')
    
	# реализуйте основную логику шага с использованием гиперпараметров
    # доработка таблицы
    
    set_data=data.drop(columns=params['target_col'])

    # Дробим таблицу на бинарные, категориальные и числовые таблицы
    binary_cat_features = set_data[['is_apartment','studio']]
    other_cat_features = set_data[['building_type_int']]
    num_features = set_data.drop(columns=['is_apartment','studio','building_type_int'])

    other_cat_cols = other_cat_features.columns.tolist()
    binary_cols = binary_cat_features.columns.tolist()
    num_cols = num_features.columns.tolist()

    ''' 
    Преобразовываем параметры в вид для обучения
    
    Вникнув в параметры CatBoost, понял что OneHotEncoder и CatBoostEncoder не нужны, 
    т.к. модель отлично делает кодирование категориальных и числовых бинарных значений сама. 
    StandardScaler не ухудшает кодирование, так что можно оставить
    Но решил оставить, т.к. еще не сильно разобрался с записью "сырых" параметров в CatBoostRegressor
    '''
    preprocessor = ColumnTransformer(
    [
        ('binary', OneHotEncoder(drop=params['one_hot_drop']), binary_cols),
        ('cat', CatBoostEncoder (return_df=False), other_cat_cols),
        ('num', StandardScaler(), num_cols)
    ],
    remainder='drop',
    verbose_feature_names_out=False
)

    model = CatBoostRegressor()

    pipeline = Pipeline(
    [
        ('preprocessor', preprocessor),
        ('model', model)
    ]
)
    pipeline.fit(set_data, data[params['target_col']])
	# сохраните обученную модель в models/train_model.pkl
    os.makedirs('models', exist_ok=True)
    with open('models/train_model.pkl', 'wb') as fd:
        joblib.dump(pipeline, fd) 


if __name__ == '__main__':
	fit_model()