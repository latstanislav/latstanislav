import json
import os

import joblib
import mlflow
import numpy as np
import pandas as pd
import yaml
from catboost import CatBoostRegressor
from dotenv import load_dotenv
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


# обучение модели
def fit_model():
    # читаем гиперпараметры
    with open("params.yaml", "r") as fd:
        params = yaml.safe_load(fd)

    # загружаем данные
    data = pd.read_csv("data/s2_data.csv")

    # выделяем таргет
    y = data[params["target_col"]]
    X = data.drop(columns=params["target_col"])

    # делим на train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Выделяем категориальные признаки
    cat_features = ["is_apartment", "studio", "building_type_int"]

    # Задаем папку для логирования временных файлов при обучении
    train_dir_path = "models/logs/catboost_training"
    os.makedirs(train_dir_path, exist_ok=True)
    # Выбираем модель с гипперпараметрами
    model = CatBoostRegressor(
        cat_features=cat_features,
        verbose=100,
        random_state=42,
        train_dir=train_dir_path,
    )
    # Обучаем, логируем в MLflow и получаем метрики
    metrics = train_and_log(model, X_train, X_test, y_train, y_test)

    # сохраняем метрики в json
    os.makedirs("metrics", exist_ok=True)
    with open("metrics/fit_model_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)


def train_and_log(model, X_train, X_test, y_train, y_test):
    """
    Обучаем модель, вычисляем метрики, логируем в mlflow и возвращает словарь метрик.
    """
    # Тренируем модель
    model.fit(X_train, y_train)

    # сохраняем обученную модель в models/train_model.pkl
    os.makedirs("models", exist_ok=True)
    with open("models/yandex_estate_model.pkl", "wb") as fd:
        joblib.dump(model, fd)

    # Предсказываем
    y_pred = model.predict(X_test)

    # Метрики для регрессии (целевая это RMSE)
    metrics_dict = {
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
        "mae": mean_absolute_error(y_test, y_pred),
        "r2": r2_score(y_test, y_pred),
    }

    # Настройка mlflow
    load_dotenv()
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = "https://storage.yandexcloud.net"
    os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
    os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")

    TRACKING_SERVER_HOST = "127.0.0.1"
    TRACKING_SERVER_PORT = 5000

    mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:{TRACKING_SERVER_PORT}")
    mlflow.set_registry_uri(f"http://{TRACKING_SERVER_HOST}:{TRACKING_SERVER_PORT}")

    EXPERIMENT_NAME = "yandex_estate"
    RUN_NAME = "yandex_estate_run"
    REGISTRY_MODEL_NAME = "yandex_estate"

    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

    if experiment is None:
        experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
    else:
        experiment_id = experiment.experiment_id

    pip_requirements = "../requirements.txt"
    signature = mlflow.models.infer_signature(X_test, y_pred)
    input_example = X_test[:10]

    with mlflow.start_run(run_name=RUN_NAME, experiment_id=experiment_id):

        mlflow.log_params(model.get_params())
        mlflow.log_metrics(metrics_dict)

        mlflow.catboost.log_model(
            cb_model=model,
            artifact_path="models",
            registered_model_name=REGISTRY_MODEL_NAME,
            signature=signature,
            input_example=input_example,
            pip_requirements=pip_requirements,
            await_registration_for=60,
        )
    return metrics_dict


if __name__ == "__main__":
    fit_model()
