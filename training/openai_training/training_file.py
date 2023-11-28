import random
import pandas as pd
from sqlalchemy.orm import Session
from database.db_data import fetch_case_study, fetch_case_study_evaluation, fetch_review_guide
from database.schema import CaseStudyEvaluation
from apis.openai_api import call_gpt_api
from training.openai_training.training_data import *


def add_grid(score_grid: str, sample_evaluation_data: str) -> str:
    grid_content = f"""\nCommunication Score grid Reference: \n{score_grid}\n"""
    data = sample_evaluation_data + grid_content
    return data


def generate_summary(instructions: str, email: str, content: str) -> tuple:
    instructions = call_gpt_api(settings.SUMMARY_MESSAGE, instructions)
    print("Instructions summary done!")
    email = call_gpt_api(settings.SUMMARY_MESSAGE, email)
    print("Email summary done!")
    content = call_gpt_api(settings.SUMMARY_MESSAGE, content)
    print("Content summary done!")
    return instructions, email, content