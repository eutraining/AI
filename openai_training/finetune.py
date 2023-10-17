import os
import openai
import json
import csv
from chatgpt_api.config import settings

openai.api_key = settings.OPENAI_API_KEY


def upload_file(filepath: str) -> str:
    file_id = openai.File.create(
        file=open(filepath, "rb"),
        purpose='fine-tune'
    )
    return file_id["id"]


def fine_tune_job(file_id: str, filename: str) -> tuple:
    model_id = openai.FineTuningJob.create(training_file=file_id, model="gpt-3.5-turbo-0613", hyperparameters={"n_epochs": settings.N_EPOCHS})
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


def process_finetune(base_path: str, filename: str) -> None:
    jsonl_files = os.listdir(base_path)
    for file in jsonl_files:
        print(file)
        f_id = upload_file(base_path + file)
        f_name = filename + file.split(".")[0]
        m_id, model_status = fine_tune_job(f_id, f_name)
        print(f"Model ID: {m_id}")
        print(f"Model Status: {model_status}")


def generate_finetune(dataset_type: str, summary_var: bool) -> None:
    base_path = "./dataset_files/"
    f_name = "./fine_tuned_model_files/"
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
    process_finetune(base_path, f_name)

