import os
from data_analysis.extraction import *
from sqlalchemy.orm import Session
from database.schema import CaseStudy, ReviewGuide, CaseStudyEvaluation


# Function for creating Case Study Record
def add_case_study(instructions: str, abbreviations: str, email: str, content: str,
                   file_name: str, session: Session) -> None:
    try:
        case_study_create = CaseStudy(
            instructions=instructions,
            abbreviations=abbreviations,
            email_instructions=email,
            context=content,
            name=file_name
        )
        session.add(case_study_create)
        session.commit()
        print("Data added to the Case Study successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        session.rollback()


# Function for creating Case Study Evaluation Record
def add_evaluation_info(case_study_id: int, overall_score: float, summary: str, communication_score: float,
                        communication_summary: str, errors_info: str, tips_to_improve: str,
                        trainee_answer: str, session: Session) -> None:
    try:
        case_study_evaluation = CaseStudyEvaluation(
            case_study_id=case_study_id,
            overall_score=overall_score,
            overall_summary=summary,
            communication_score=communication_score,
            communication_summary=communication_summary,
            communication_errors=errors_info,
            communication_tips=tips_to_improve,
            trainee_answer=trainee_answer
        )
        session.add(case_study_evaluation)
        session.commit()
        print("Data added to the Evaluation Info successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        session.rollback()


# Function for creating Review Guide Record
def add_review_guide(case_study_id: int, recommendations: str, score_grid: str, session: Session) -> None:
    try:
        review_guide_create = ReviewGuide(
            case_study_id=case_study_id,
            recommendations=recommendations,
            score_grid=score_grid
        )
        session.add(review_guide_create)
        session.commit()
        print("Data added to the Review Guide successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        session.rollback()


def add_extracted_info_database(base_path: str, session: Session) -> None:
    # List all the Case Studies Directories
    case_studies_path = os.listdir(base_path)
    # Iterate over all the case studies
    for ind, cs in enumerate(case_studies_path):
        # CASE STUDIES FILES
        case_study_path = base_path + "/" + cs
        case_study_files = sorted(os.listdir(case_study_path))
        # CASE STUDY NAME AND ID
        file_name = case_study_files[0].split(".")[0].strip()
        case_study_id = ind + 1
        print(f"Case Study ID: {case_study_id}")
        # CASE STUDY INFO EXTRACT
        case_study = case_study_path + "/" + case_study_files[0]
        case_study_info = read_docx(case_study)
        instructions, abbreviations, email, content = case_study_extract(case_study_info)
        ''''''
        add_case_study(instructions, abbreviations, email, content, file_name, session)
        ''''''
        # REVIEW GUIDE INFO EXTRACT
        review_guide = case_study_path + "/" + case_study_files[1]
        review_guide_info = read_docx(review_guide)
        print(review_guide)
        score_grid, recommendations_solution = review_guide_extract(review_guide_info)
        ''''''
        add_review_guide(case_study_id, recommendations_solution, score_grid, session)
        ''''''
        # CASE STUDY EVALUATION AND TRAINEE'S ANSWER
        for i in range(0, len(case_study_files[2:]), 2):
            trainee_file = case_study_path + "/" + case_study_files[i + 2]
            evaluation_file = case_study_path + "/" + case_study_files[i + 3]
            print(f"Trainee's File : {trainee_file}")
            print(f"Evaluation File : {evaluation_file}\n")
            # TRAINEE'S ANSWER
            trainee_info = read_docx(trainee_file)
            case_study_name, answer_content = trainee_answer_extractor(trainee_info)
            # EVALUATION INFO
            evaluation_info = read_docx(evaluation_file)
            overall_score, summary, communication_score, communication_summary, \
                errors_info, tips_to_improve = evaluation_info_extract(evaluation_info)
            ''''''
            add_evaluation_info(case_study_id, overall_score, summary, communication_score, communication_summary,
                                errors_info, tips_to_improve, answer_content, session)
            ''''''



