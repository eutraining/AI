import pandas as pd
import numpy as np
import os
import re
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


def find_actual_score(pattern: str, text: str) -> float:
    score = re.findall(pattern, text)[0]
    score = float(score)
    return score


def find_predicted_score(pattern_1: str, pattern_2: str, text: str) -> float:
    score = re.findall(pattern_1, text)
    if score:
        score = float(score[0])
        return score
    score = re.findall(pattern_2, text)
    if len(score) > 2:
        score = score[-2]
    else:
        score = score[0]
    score = float(score)
    return score


def set_limit(value: float) -> tuple:
    min_lim = value - 1
    max_lim = value + 1
    return min_lim, max_lim


def get_accuracy(df_path: str, actual_pattern: str, predicted_pattern_1: str, predicted_pattern_2: str) -> list:
    df = pd.read_csv(df_path)
    actual_list = []
    predicted_list = []
    tokens = 0
    total = 0
    for ind, row in df.iterrows():
        actual = row["Actual"]
        predicted = row["Predicted"]
        try:
            token = row["Input Token Count"] + row["Output Token Count"]
        except KeyError:
            token = 0
        if pd.isnull(predicted):
            continue
        actual_score = find_actual_score(actual_pattern, actual)
        predicted_score = find_predicted_score(predicted_pattern_1, predicted_pattern_2, predicted)
        """R2 Score"""
        actual_list.append(actual_score)
        predicted_list.append(predicted_score)
        """Average Token"""
        tokens += token
        total += 1

    actual_list = np.array(actual_list)
    predicted_list = np.array(predicted_list)
    approach = df_path.split("/")[-1].split(".")[0]
    """MAE, MSE, RMSE Loss"""
    mae = mean_absolute_error(actual_list, predicted_list)
    mse = mean_squared_error(actual_list, predicted_list)
    rmse = mean_squared_error(actual_list, predicted_list, squared=False)
    """"""
    # r_squared = round(r2_score(actual_list, predicted_list), 2)
    """"""
    avg_token = round(tokens / total, 2)
    return [approach, mae, mse, rmse, avg_token]


if __name__ == "__main__":
    actual_score_pattern = r"(\d+\.\d+)"
    predicted_score_pattern_1 = r"(\d+\.\d+)"
    predicted_score_pattern_2 = r"(\d+\.|\d+)"

    base_path = "../predicted_files/singleton/summary/"
    path_csv = os.listdir(base_path)

    accuracy_df = []
    output_path = "../test/accuracy_score.csv"

    for path in path_csv:
        csv_path = base_path + path
        if path.find("communication_score") != -1:
            accuracy_val = get_accuracy(csv_path, actual_score_pattern, predicted_score_pattern_1, predicted_score_pattern_2)
            accuracy_df.append(accuracy_val)
        elif path.find("overall_score") != -1:
            accuracy_val = get_accuracy(csv_path, actual_score_pattern, predicted_score_pattern_1, predicted_score_pattern_2)
            accuracy_df.append(accuracy_val)

    dataframe = pd.DataFrame(accuracy_df, columns=["Approach", "MAE Loss", "MES Loss", "RMSE Loss", "Average Token"])
    dataframe.to_csv(output_path, index=False)
