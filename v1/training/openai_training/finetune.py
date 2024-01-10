import os
import openai
import json
import pandas as pd
from config import settings
from training.openai_training.training_data import create_jsonl_file

openai.api_key = settings.OPENAI_API_KEY


def upload_file(filepath: str) -> str:
    file_id = openai.File.create(
        file=open(filepath, "rb"),
        purpose='fine-tune'
    )
    return file_id["id"]


def fine_tune_job(file_id: str, filename: str, model: str) -> tuple:
    model_id = openai.FineTuningJob.create(training_file=file_id, model=model, hyperparameters={"n_epochs": settings.N_EPOCHS})
    # Wait for the fine-tuning job to finish
    while True:
        status = openai.FineTuningJob.retrieve(id=model_id.id)
        print(status["status"])
        if status["status"] in ["succeeded", "failed"]:
            break
    # Download the fine-tuned model
    fine_tuned_model = openai.FineTuningJob.retrieve(id=model_id.id)
    # Save the fine-tuned model to a file
    with open(filename + ".json", "w") as f:
        json.dump(fine_tuned_model, f)
    return model_id, status


def process_finetune(base_path: str, filename: str, model: str) -> None:
    jsonl_files = os.listdir(base_path)
    for file in jsonl_files:
        print(file)
        f_id = upload_file(base_path + file)
        f_name = filename + file.split(".")[0]
        m_id, model_status = fine_tune_job(f_id, f_name, model)
        print(f"Model ID: {m_id}")
        print(f"Model Status: {model_status}")


def generate_finetune(dataset_type: str, summary_var: bool, model="gpt-3.5-turbo-0613") -> None:
    base_path = "./dataset/"
    f_name = "./models/"
    if dataset_type == "clubbed":
        base_path += "clubbed/"
        f_name += "clubbed/"
    elif dataset_type == "singleton":
        base_path += "singleton/"
        f_name += "singleton/"
    if summary_var:
        base_path += "summary/"
        f_name += "summary/"
    else:
        base_path += "non_summary/"
        f_name += "non_summary/"
    process_finetune(base_path, f_name, model)


# Function to read a JSONL file and assign an index to each line
def read_jsonl_with_index(file_path) -> list:
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    result = []
    for index, line in enumerate(lines):
        try:
            data = json.loads(line)
            result.append(data)
        except json.JSONDecodeError:
            print(f"Skipping line {index}: Invalid JSON")

    return result


def babbage_format_data(data: dict) -> dict:
    messages = data["messages"]
    system = messages[0]["content"]
    user = messages[1]["content"]
    assistant = messages[2]["content"]
    prompt = system + "\n\n" + user
    data = {
        "prompt": prompt,
        "completion": assistant
    }
    return data


def create_babbage_dataset(split: str) -> None:
    df = pd.read_csv(f"./dataset/{split}.csv")
    evaluation_ids = []
    result_comm = read_jsonl_with_index("./dataset/singleton/summary/communication_score_v2_sample.jsonl")
    result_overall = read_jsonl_with_index("./dataset/singleton/summary/overall_score_v2_sample.jsonl")
    for ind, row in df.iterrows():
        evaluation_ids.append(row["Evaluation ID"])
    communication_score_file = []
    overall_score_file = []
    for e_id in evaluation_ids:
        comm_data = babbage_format_data(result_comm[e_id-1])
        overall_data = babbage_format_data(result_overall[e_id-1])
        communication_score_file.append(comm_data)
        overall_score_file.append(overall_data)
    create_jsonl_file(communication_score_file,
                      f"./dataset/singleton/summary/communication_score_babbage_{split}_sample.jsonl")
    create_jsonl_file(overall_score_file, f"./dataset/singleton/summary/overall_score_babbage_{split}_sample.jsonl")


def babbage_finetune(metric: str) -> None:
    file_path = ""
    if metric == "overall":
        file_path = "./dataset/singleton/summary/overall_score_babbage_train_sample.jsonl"
    elif metric == "communication":
        file_path = "./dataset/singleton/summary/communication_score_babbage_train_sample.jsonl"
    f_id = upload_file(file_path)
    f_name = "./models/singleton/summary/" + file_path.split("/")[4].split(".")[0] + f"_{settings.N_EPOCHS}"
    m_id, model_status = fine_tune_job(f_id, f_name, "babbage-002")
    print(f"Model ID: {m_id}")
    print(f"Model Status: {model_status}")


def create_gpt_dataset(split: str) -> None:
    df = pd.read_csv(f"./dataset/{split}.csv")
    evaluation_ids = []
    result_comm = read_jsonl_with_index("./dataset/singleton/summary/communication_score_v2_sample_grid.jsonl")
    result_overall = read_jsonl_with_index("./dataset/singleton/summary/overall_score_v2_sample_grid.jsonl")
    for ind, row in df.iterrows():
        evaluation_ids.append(row["Evaluation ID"])
    communication_score_file = []
    overall_score_file = []
    for e_id in evaluation_ids:
        comm_data = result_comm[e_id-1]
        overall_data = result_overall[e_id-1]
        communication_score_file.append(comm_data)
        overall_score_file.append(overall_data)
    create_jsonl_file(communication_score_file,
                      f"./dataset/singleton/summary/communication_score_gpt3.5_{split}_sample_grid.jsonl")
    create_jsonl_file(overall_score_file, f"./dataset/singleton/summary/overall_score_gpt3.5_{split}_sample_grid.jsonl")


def gpt_finetune_train(metric: str) -> None:
    file_path = ""
    if metric == "overall":
        file_path = "./dataset/singleton/summary/overall_score_gpt3.5_train_sample.jsonl"
    elif metric == "communication":
        file_path = "./dataset/singleton/summary/communication_score_gpt3.5_train_sample.jsonl"
    f_id = upload_file(file_path)
    f_name = "./models/singleton/summary/" + file_path.split("/")[4].split(".")[0] + f"_{settings.N_EPOCHS}"
    m_id, model_status = fine_tune_job(f_id, f_name, "gpt-3.5-turbo-0613")
    print(f"Model ID: {m_id}")
    print(f"Model Status: {model_status}")


