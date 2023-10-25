import random
import pandas as pd
from sqlalchemy.orm import Session
from database.db_data import fetch_case_study, fetch_case_study_evaluation, fetch_review_guide
from database.schema import CaseStudyEvaluation
from chatgpt_api.openai_api import call_gpt_api
from openai_training.training_data import *


def generate_summary(instructions: str, email: str, content: str) -> tuple:
    instructions = call_gpt_api(settings.SUMMARY_MESSAGE, instructions)
    email = call_gpt_api(settings.SUMMARY_MESSAGE, email)
    content = call_gpt_api(settings.SUMMARY_MESSAGE, content)
    return instructions, email, content


def generate_training_clubbed(case_studies_id: list, session: Session, summary_var: bool) -> None:
    # JSONL Files list
    overall_score_summary_file = []
    communication_score_summary_file = []
    tips_errors_file = []

    dir_name = "non_summary"

    for cs_id in case_studies_id:
        name, instructions, abbreviations, email_instructions, context = fetch_case_study(cs_id, session)
        ''' Case Study Summary'''
        if summary_var:
            instructions, email_instructions, context = generate_summary(instructions, email_instructions, context)
            dir_name = "summary"
        evaluations_records = fetch_case_study_evaluation(cs_id, session)
        for record in evaluations_records:
            eval_id, overall_score, overall_summary, communication_score, communication_summary, communication_errors, \
               communication_tips, trainee_answer = record
            # Create Evaluation Sample and Other Data
            sample_evaluation_data = create_evaluation_sample(name, instructions, abbreviations,
                                                              email_instructions, context, trainee_answer)
            overall_content = create_overall_content(overall_summary, overall_score)
            communication_content = create_communication_content(communication_summary, communication_score)
            tips_errors_content = create_tips_errors(communication_tips, communication_errors)
            # JSON Data Fetching
            overall_score_summary = create_overall_score(sample_evaluation_data, overall_content)
            communication_score_summary = create_communication_score(sample_evaluation_data, communication_content)
            tips_errors_dict = create_tips_errors_content(sample_evaluation_data, tips_errors_content)
            # JSON Data Appending
            overall_score_summary_file.append(overall_score_summary)
            communication_score_summary_file.append(communication_score_summary)
            tips_errors_file.append(tips_errors_dict)

    # JSONL Filenames
    overall_score_summary_jsonl_filename = f"./dataset_files/clubbed/{dir_name}/overall_score_summary.jsonl"
    communication_score_summary_jsonl_filename = f"./dataset_files/clubbed/{dir_name}/communication_score_summary.jsonl"
    tips_errors_summary_jsonl_filename = f"./dataset_files/clubbed/{dir_name}/tips_errors.jsonl"
    # Creating JSONL Files
    create_jsonl_file(overall_score_summary_file, overall_score_summary_jsonl_filename)
    create_jsonl_file(communication_score_summary_file, communication_score_summary_jsonl_filename)
    create_jsonl_file(tips_errors_file, tips_errors_summary_jsonl_filename)


def generate_training_singleton(case_studies_id: list, session: Session, summary_var: bool) -> None:
    # JSONL Files list
    overall_score_file = []
    # overall_summary_file = []
    communication_score_file = []
    # communication_summary_file = []
    # tips_errors_file = []

    dir_name = "non_summary"

    for cs_id in case_studies_id:
        name, instructions, abbreviations, email_instructions, context = fetch_case_study(cs_id, session)
        score_grid, sample_solution = fetch_review_guide(cs_id, session)
        ''' Case Study Summary'''
        if summary_var:
            instructions, email_instructions, context = generate_summary(instructions, email_instructions, context)
            dir_name = "summary"
        evaluations_records = fetch_case_study_evaluation(cs_id, session)
        for record in evaluations_records:
            eval_id, overall_score, overall_summary, communication_score, communication_summary, communication_errors, \
                communication_tips, trainee_answer = record
            # Create Evaluation Sample and Other Data
            sample_evaluation_data = create_evaluation_sample(name, instructions, abbreviations,
                                                              email_instructions, context, trainee_answer,
                                                              sample_solution)
            overall_score_content = create_score_content("Overall", overall_score)
            # overall_summary_content = create_summary_content("Overall", overall_summary)
            communication_score_content = create_score_content("Communication", communication_score)
            # communication_summary_content = create_summary_content("Communication", communication_summary)
            # tips_errors_content = create_tips_errors(communication_tips, communication_errors)

            """JSON Data Fetching"""
            score_content = create_dict_data(settings.OVERALL_SCORE_MESSAGE, sample_evaluation_data,
                                             overall_score_content)
            # summary_content = create_dict_data(settings.OVERALL_SUMMARY_MESSAGE, sample_evaluation_data,
            #                                    overall_summary_content)
            communication_score_content = create_dict_data(settings.COMMUNICATION_SCORE_MESSAGE, sample_evaluation_data,
                                                           communication_score_content)
            # communication_summary_content = create_dict_data(settings.COMMUNICATION_SUMMARY_MESSAGE,
            #                                                  sample_evaluation_data, communication_summary_content)
            # tips_errors_dict = create_tips_errors_content(sample_evaluation_data, tips_errors_content)
            """JSON Data Appending"""
            overall_score_file.append(score_content)
            # overall_summary_file.append(summary_content)
            communication_score_file.append(communication_score_content)
            # communication_summary_file.append(communication_summary_content)
            # tips_errors_file.append(tips_errors_dict)

    '''JSONL Filenames'''
    overall_score_jsonl_filename = f"./dataset_files/singleton/{dir_name}/overall_score_v2_sample.jsonl"
    # overall_summary_jsonl_filename = f"./dataset_files/singleton/{dir_name}/overall_summary.jsonl"
    communication_score_jsonl_filename = f"./dataset_files/singleton/{dir_name}/communication_score_v2_sample.jsonl"
    # communication_summary_jsonl_filename = f"./dataset_files/singleton/{dir_name}/communication_summary.jsonl"
    # tips_errors_summary_jsonl_filename = f"./dataset_files/singleton/{dir_name}/tips_errors.jsonl"
    '''Creating JSONL Files'''
    create_jsonl_file(overall_score_file, overall_score_jsonl_filename)
    # create_jsonl_file(overall_summary_file, overall_summary_jsonl_filename)
    create_jsonl_file(communication_score_file, communication_score_jsonl_filename)
    # create_jsonl_file(communication_summary_file, communication_summary_jsonl_filename)
    # create_jsonl_file(tips_errors_file, tips_errors_summary_jsonl_filename)


def random_generation(data: list) -> tuple:
    # Calculate the count of numbers for each group
    total_count = len(data)
    count_80_percent = int(0.8 * total_count)

    # Shuffle the list for 80% of the values
    random.shuffle(data)
    train_data = data[:count_80_percent]

    # Shuffle the remaining 20% of the values
    test_data = data[count_80_percent:]
    random.shuffle(test_data)

    return train_data, test_data


def assign_values(record: CaseStudyEvaluation) -> tuple:
    cs_id = record.case_study_id
    overall_score = record.overall_score
    overall_summary = record.overall_summary
    communication_score = record.communication_score
    communication_summary = record.communication_summary
    communication_errors = record.communication_errors
    communication_tips = record.communication_tips
    trainee_answer = record.trainee_answer
    return cs_id, overall_score, overall_summary, communication_score, communication_summary, communication_errors, \
        communication_tips, trainee_answer


def train_validation_split(evaluation_studies_id: list, session: Session) -> None:
    columns = ["CS ID", "Name", "Instructions", "Abbreviations", "Email Instructions", "Content",
               "Evaluation ID", "Overall Score", "Overall Summary", "Communication Score",
               "Communication Summary", "Communication Errors", "Communication Tips", "Trainee's Ans"]
    train_df = []
    test_df = []
    train_data, test_data = random_generation(evaluation_studies_id)

    for ev_id in train_data:
        record = session.query(CaseStudyEvaluation).get(ev_id)
        cs_id, overall_score, overall_summary, communication_score, communication_summary, communication_errors, \
            communication_tips, trainee_answer = assign_values(record)
        print(cs_id, ev_id)
        name, instructions, abbreviations, email_instructions, context = fetch_case_study(cs_id, session)
        train_df.append([cs_id, name, instructions, abbreviations, email_instructions, context,
                         ev_id, overall_score, overall_summary, communication_score, communication_summary,
                         communication_errors, communication_tips, trainee_answer])

    for ev_id in test_data:
        record = session.query(CaseStudyEvaluation).get(ev_id)
        cs_id, overall_score, overall_summary, communication_score, communication_summary, communication_errors, \
            communication_tips, trainee_answer = assign_values(record)
        print(cs_id, ev_id)
        name, instructions, abbreviations, email_instructions, context = fetch_case_study(cs_id, session)
        test_df.append([cs_id, name, instructions, abbreviations, email_instructions, context,
                        ev_id, overall_score, overall_summary, communication_score, communication_summary,
                        communication_errors, communication_tips, trainee_answer])

    train_df = pd.DataFrame(train_df, columns=columns)
    test_df = pd.DataFrame(test_df, columns=columns)

    train_df.to_csv("./dataset_files/train.csv", index=False)
    test_df.to_csv("./dataset_files/test.csv", index=False)
