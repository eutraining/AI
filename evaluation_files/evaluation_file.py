from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_analysis.schema import CaseStudy
from fetch_db_data import fetch_case_study, fetch_case_study_evaluation
from openai_api import call_gpt_api
from config import settings
from make_evaluation_data import *

engine = create_engine('sqlite:///eutraining.db')
Session = sessionmaker(bind=engine)
session = Session()

case_studies_id = session.query(CaseStudy.case_study_id).all()
case_studies_id = [value[0] for value in case_studies_id]

# JSONL Files list
overall_score_summary_file = [["Actual", "Predicted"]]
communication_score_summary_file = [["Actual", "Predicted"]]
tips_errors_file = [["Actual", "Predicted"]]

for cs_id in case_studies_id:
    name, instructions, abbreviations, email_instructions, context = fetch_case_study(cs_id, session)
    ''' Case Study Summary'''
    evaluations_records = fetch_case_study_evaluation(cs_id, session)
    for record in evaluations_records:
        overall_score, overall_summary, communication_score, communication_summary, communication_errors,\
            communication_tips, trainee_answer = record
        # Create Evaluation Sample and Other Data
        sample_evaluation_data = create_evaluation_sample(name, instructions, abbreviations,
                                                          email_instructions, context, trainee_answer)
        overall_content = create_overall_content(overall_summary, overall_score)
        communication_content = create_communication_content(communication_summary, communication_score)
        tips_errors_content = create_tips_errors(communication_tips, communication_errors)
        # Predicted Data Fetching
        overall_score_summary = call_gpt_api(settings.OVERALL_SCORE_SUMMARY_MESSAGE, overall_content)
        communication_score_summary = call_gpt_api(settings.COMMUNICATION_SCORE_SUMMARY_MESSAGE, communication_content)
        tips_errors_dict = call_gpt_api(settings.TIPS_ERRORS_MESSAGE, tips_errors_content)
        # Actual - Predicted Data Appending
        overall_score_summary_file.append([overall_content, overall_score_summary])
        communication_score_summary_file.append([communication_content, communication_score_summary])
        tips_errors_file.append([tips_errors_content, tips_errors_dict])

# JSONL Filenames
overall_score_summary_jsonl_filename = "../predicted_files/overall_score_summary.csv"
communication_score_summary_jsonl_filename = "../predicted_files/communication_score_summary.csv"
tips_errors_summary_jsonl_filename = "../predicted_files/tips_errors.csv"
# Creating JSONL Files
create_csv_file(overall_score_summary_file, overall_score_summary_jsonl_filename)
create_csv_file(communication_score_summary_file, communication_score_summary_jsonl_filename)
create_csv_file(tips_errors_file, tips_errors_summary_jsonl_filename)

session.close()
