import pandas as pd
import os
import re


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


def get_accuracy(df_path: str, actual_pattern: str, predicted_pattern_1: str, predicted_pattern_2: str):
    df = pd.read_csv(df_path)
    total = 0
    correct = 0
    for ind, row in df.iterrows():
        actual = row["Actual"]
        predicted = row["Predicted"]
        if pd.isnull(predicted):
            continue
        actual_score = find_actual_score(actual_pattern, actual)
        predicted_score = find_predicted_score(predicted_pattern_1, predicted_pattern_2, predicted)
        min_limit, max_limit = set_limit(actual_score)
        if min_limit <= predicted_score <= max_limit:
            correct += 1
        total += 1
    print(f"CSV Path: {df_path} -> {(correct / total) * 100}")


if __name__ == "__main__":
    actual_score_pattern = r"(\d+\.\d+)"
    predicted_score_pattern_1 = r"(\d+\.\d+)"
    predicted_score_pattern_2 = r"(\d+\.|\d+)"

    base_path = "E:/Freelancing/AXEOM/Axeom_EUTraining/ax16-eutraining/predicted_files/singleton/summary/"
    path_csv = os.listdir(base_path)

    for path in path_csv:
        csv_path = base_path + path
        if path.find("communication_score") != -1:
            get_accuracy(csv_path, actual_score_pattern, predicted_score_pattern_1, predicted_score_pattern_2)
        elif path.find("overall_score") != -1:
            get_accuracy(csv_path, actual_score_pattern, predicted_score_pattern_1, predicted_score_pattern_2)
