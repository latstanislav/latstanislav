import json
import os

import joblib
import pandas as pd
import yaml
from sklearn.model_selection import KFold, cross_validate


# оценка качества модели
def evaluate_model():
    # прочитайте файл с гиперпараметрами params.yaml
    with open("params.yaml", "r") as fd:
        params = yaml.safe_load(fd)
    # загрузите результат прошлого шага: fitted_model.pkl
    data = pd.read_csv("data/s2_data.csv")
    set_data = data.drop(columns=params["target_col"])

    with open("models/yandex_estate_model.pkl", "rb") as fd:
        pipeline = joblib.load(fd)
    # реализуйте основную логику шага с использованием прочтённых гиперпараметров
    cv_strategy = KFold(params["n_splits"], shuffle=True, random_state=42)
    cv_res = cross_validate(
        pipeline,
        set_data,
        data[params["target_col"]],
        cv=cv_strategy,
        n_jobs=params["n_jobs"],
        scoring=params["metrics"],
    )
    for key, value in cv_res.items():
        cv_res[key] = round(value.mean(), 3)
    # сохраните результат кросс-валидации в cv_res.json
    os.makedirs("cv_results", exist_ok=True)
    with open("cv_results/cv_res_new.json", "w") as f:
        json.dump(cv_res, f, indent=2)


if __name__ == "__main__":
    evaluate_model()
