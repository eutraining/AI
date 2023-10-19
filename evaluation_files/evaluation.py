import tiktoken
from sqlalchemy.orm import Session
from database.db_data import fetch_case_study, fetch_case_study_evaluation
from chatgpt_api.openai_api import call_gpt_api
from chatgpt_api.config import settings
from evaluation_files.evaluation_data import *
from openai_training.training_file import generate_summary
from openai_training.training_data import create_score_content, create_summary_content


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(string))
    return num_tokens


def add_summary(sample_evaluation: str, summary: str, metric: str) -> str:
    metric_data = f"\n\n{metric} Summary: \n{summary}\n"
    data = sample_evaluation + metric_data
    return data


def generate_evaluation_clubbed(case_studies_id: list, session: Session, summary_var: bool) -> None:
    # JSONL Files list
    overall_score_summary_file = [["ID", "Actual", "Predicted", "Token Count"]]
    communication_score_summary_file = [["ID", "Actual", "Predicted", "Token Count"]]
    tips_errors_file = [["ID", "Actual", "Predicted", "Token Count"]]

    dir_name = "non_summary"

    for cs_id in case_studies_id:
        print("Case Study ID", cs_id)
        name, instructions, abbreviations, email_instructions, context = fetch_case_study(cs_id, session)
        ''' Case Study Summary'''
        if summary_var:
            instructions, email_instructions, context = generate_summary(instructions, email_instructions, context)
            dir_name = "summary"
        evaluations_records = fetch_case_study_evaluation(cs_id, session)
        for record in evaluations_records:
            eval_id, overall_score, overall_summary, communication_score, communication_summary, communication_errors,\
                communication_tips, trainee_answer = record

            # Create Evaluation Sample Data
            sample_evaluation_data = create_evaluation_sample(name, instructions, abbreviations,
                                                              email_instructions, context, trainee_answer)
            # Actual Data Fetching
            overall_content = create_overall_content(overall_summary, overall_score)
            communication_content = create_communication_content(communication_summary, communication_score)
            tips_errors_content = create_tips_errors(communication_tips, communication_errors)
            # Predicted Data Fetching
            overall_score_summary = call_gpt_api(settings.OVERALL_SCORE_SUMMARY_MESSAGE, sample_evaluation_data)
            communication_score_summary = call_gpt_api(settings.COMMUNICATION_SCORE_SUMMARY_MESSAGE, sample_evaluation_data)
            tips_errors_dict = call_gpt_api(settings.TIPS_ERRORS_MESSAGE,  sample_evaluation_data)
            # Actual - Predicted Data Appending
            overall_score_summary_file.append([eval_id, overall_content, overall_score_summary])
            communication_score_summary_file.append([eval_id, communication_content, communication_score_summary])
            tips_errors_file.append([eval_id, tips_errors_content, tips_errors_dict])

    # JSONL Filenames
    overall_score_summary_csv_filename = f"./predicted_files/clubbed/{dir_name}/overall_score_summary.csv"
    communication_score_summary_csv_filename = f"./predicted_files/clubbed/{dir_name}/communication_score_summary.csv"
    tips_errors_summary_csv_filename = f"./predicted_files/clubbed/{dir_name}/tips_errors.csv"
    # Creating JSONL Files
    create_csv_file(overall_score_summary_file, overall_score_summary_csv_filename)
    create_csv_file(communication_score_summary_file, communication_score_summary_csv_filename)
    create_csv_file(tips_errors_file, tips_errors_summary_csv_filename)


def generate_evaluation_singleton(case_studies_id: list, session: Session, summary_var: bool) -> None:
    # JSONL Files list
    overall_score_file = [["ID", "Actual", "Predicted", "Input Token Count", "Output Token Count"]]
    overall_summary_file = [["ID", "Actual", "Predicted", "Input Token Count", "Output Token Count"]]
    communication_score_file = [["ID", "Actual", "Predicted", "Input Token Count", "Output Token Count"]]
    communication_summary_file = [["ID", "Actual", "Predicted", "Input Token Count", "Output Token Count"]]
    tips_errors_file = [["ID", "Actual", "Predicted", "Input Token Count", "Output Token Count"]]

    dir_name = "non_summary"

    for cs_id in case_studies_id:
        name, instructions, abbreviations, email_instructions, context = fetch_case_study(cs_id, session)
        print(f"Case Study ID: {cs_id}")
        ''' Case Study Summary'''
        if summary_var:
            instructions, email_instructions, context = generate_summary(instructions, email_instructions, context)
            dir_name = "summary"

        evaluations_records = fetch_case_study_evaluation(cs_id, session)

        for record in evaluations_records:
            eval_id, overall_score, overall_summary, communication_score, communication_summary, communication_errors, \
                communication_tips, trainee_answer = record
            print(f"Evaluation ID: {eval_id}")
            # Create Evaluation Sample and Other Data
            sample_evaluation_data = create_evaluation_sample(name, instructions, abbreviations,
                                                              email_instructions, context, trainee_answer)
            # Actual Data Fetching
            overall_score_content = create_score_content("Overall", overall_score)
            overall_summary_content = create_summary_content("Overall", overall_summary)
            actual_communication_score_content = create_score_content("Communication", communication_score)
            actual_communication_summary_content = create_summary_content("Communication", communication_summary)
            actual_tips_errors_content = create_tips_errors(communication_tips, communication_errors)

            # GPT Data Fetching
            summary_content = call_gpt_api(settings.OVERALL_SUMMARY_MESSAGE, sample_evaluation_data)
            score_evaluation = add_summary(sample_evaluation_data, summary_content, "Overall")
            score_content = call_gpt_api(settings.OVERALL_SCORE_MESSAGE, score_evaluation)  # "ft:gpt-3.5-turbo-0613:personal::8AdMdd1c"
            communication_summary_content = call_gpt_api(settings.COMMUNICATION_SUMMARY_MESSAGE, sample_evaluation_data)
            communication_score_evaluation = add_summary(sample_evaluation_data, communication_summary_content, "Communication")
            communication_score_content = call_gpt_api(settings.COMMUNICATION_SCORE_MESSAGE, communication_score_evaluation)  # "ft:gpt-3.5-turbo-0613:personal::8Ad342wv"
            tips_errors = call_gpt_api(settings.TIPS_ERRORS_MESSAGE, sample_evaluation_data)

            # Input Token Count
            summary_content_input_token = num_tokens_from_string(settings.OVERALL_SUMMARY_MESSAGE + sample_evaluation_data)
            score_content_input_token = num_tokens_from_string(settings.OVERALL_SCORE_MESSAGE + score_evaluation)
            communication_input_summary_content_token = num_tokens_from_string(settings.COMMUNICATION_SUMMARY_MESSAGE + sample_evaluation_data)
            communication_input_score_content_token = num_tokens_from_string(settings.COMMUNICATION_SCORE_MESSAGE + communication_score_evaluation)
            tips_errors_input_token = num_tokens_from_string(settings.TIPS_ERRORS_MESSAGE + sample_evaluation_data)

            # Output Token Count
            summary_content_output_token = num_tokens_from_string(summary_content)
            score_content_output_token = num_tokens_from_string(score_content)
            communication_output_summary_content_token = num_tokens_from_string(communication_summary_content)
            communication_output_score_content_token = num_tokens_from_string(communication_score_content)
            tips_errors_output_token = num_tokens_from_string(tips_errors)

            # CSV Data Appending
            overall_score_file.append([eval_id, overall_score_content, score_content, score_content_input_token,
                                       score_content_output_token])
            overall_summary_file.append([eval_id, overall_summary_content, summary_content, summary_content_input_token,
                                         summary_content_output_token])
            communication_score_file.append([eval_id, actual_communication_score_content, communication_score_content,
                                             communication_input_score_content_token, communication_output_score_content_token])
            communication_summary_file.append([eval_id, actual_communication_summary_content,
                                               communication_summary_content, communication_input_summary_content_token,
                                               communication_output_summary_content_token])
            tips_errors_file.append([eval_id, actual_tips_errors_content, tips_errors, tips_errors_input_token,
                                     tips_errors_output_token])

    # CSV Filenames
    overall_score_csv_filename = f"./predicted_files/singleton/{dir_name}/overall_score_non.csv"
    overall_summary_csv_filename = f"./predicted_files/singleton/{dir_name}/overall_summary_non.csv"
    communication_score_csv_filename = f"./predicted_files/singleton/{dir_name}/communication_score_non.csv"
    communication_summary_csv_filename = f"./predicted_files/singleton/{dir_name}/communication_summary_non.csv"
    tips_errors_summary_csv_filename = f"./predicted_files/singleton/{dir_name}/tips_errors_non.csv"

    # Creating CSV Files
    create_csv_file(overall_score_file, overall_score_csv_filename)
    create_csv_file(overall_summary_file, overall_summary_csv_filename)
    create_csv_file(communication_score_file, communication_score_csv_filename)
    create_csv_file(communication_summary_file, communication_summary_csv_filename)
    create_csv_file(tips_errors_file, tips_errors_summary_csv_filename)


