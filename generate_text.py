from gpt_calls import generate_section_gpt, generate_summary_gpt
from models.models import CommunicationsExamInfo
from utils import read_docx, case_study_extract, fetch_prompt_message
from gpt_calls import generate_candidate_task_gpt, extract_point_of_views_gpt, extract_target_audience_gpt
from config import settings

import re
from enum import Enum

class Sections(Enum):
    OBSERVATIONS = "Key observations"
    GRAMMAR = "Grammar errors"
    TIPS = "Key tips to improve"


def generate_full_text(candidate_response: str, exam_doc_path: str, perfect_response: str = "") -> tuple:
    """
    Generates the evaluation text and a summary based on the candidate's response and exam document.
    Optionally compares with a perfect response.

    Args:
    candidate_response (str): The candidate's response text.
    exam_doc_path (str): The file path to the exam document.
    perfect_response (str, optional): A perfect response for comparison.

    Returns:
    tuple: A tuple containing the evaluation text and summary.
    """
    exam_info = get_exam_info(exam_doc_path)
    add_candidate_abbreviations(candidate_response, exam_info)
    evaluation_text = generate_evaluation_text(candidate_response, exam_info, perfect_response)
    summary_text = generate_summary_gpt(evaluation_text)

    return evaluation_text, summary_text

def generate_evaluation_text(candidate_response: str, exam_info: CommunicationsExamInfo, perfect_response: str = "") -> str:
    """
    Generates different sections of the evaluation text

    Args:
    candidate_response (str): The candidate's response text.
    exam_info (CommunicationsExamInfo): Information about the exam.
    perfect_response (str, optional): A perfect response for comparison.

    Returns:
    str: The complete evaluation text comprising various sections.
    """

    text_until_now = ""

    # Generate observations section
    observations_guideline = fetch_prompt_message(settings.OBSERVATIONS_GUIDELINE_PATH)
    observations = generate_section_gpt(
        Sections.OBSERVATIONS.value, candidate_response, exam_info, text_until_now, observations_guideline, perfect_response
    )
    text_until_now += observations + "\n\n"

    # Generate grammar section
    grammar_guideline = fetch_prompt_message(settings.GRAMMAR_GUIDELINE_PATH)
    grammar = generate_section_gpt(
        Sections.GRAMMAR.value, candidate_response, exam_info, text_until_now, grammar_guideline, perfect_response
    )
    text_until_now += grammar + "\n\n"

    # Generate tips section
    tips_guideline = fetch_prompt_message(settings.TIPS_GUIDELINE_PATH)
    tips = generate_section_gpt(
        Sections.TIPS.value, candidate_response, exam_info, text_until_now, tips_guideline, perfect_response
    )
    text_until_now += tips + "\n\n"

    return text_until_now

def add_candidate_abbreviations(candidate_response: str, exam_info: CommunicationsExamInfo) -> None:
    """
    Extracts and adds candidate abbreviations to exam_info.

    Args:
    candidate_response (str): The text of the candidate's response.
    exam_info (CommunicationsExamInfo): The exam info object to update with abbreviations.
    """
    pattern = r'\(([A-Z]{2,})\)\s*([\w\s]+)|([\w\s]+)\s*\(([A-Z]{2,})\)'
    matches = re.findall(pattern, candidate_response)
    acronyms_and_explanations = {acronym: explanation.strip() for acronym, explanation in matches}
    acronyms_str = '\n'.join([f'{acronym}: {explanation}' for acronym, explanation in acronyms_and_explanations.items()])
    exam_info.abbreviations += "\n" + acronyms_str

def get_exam_info(case_study_path: str) -> CommunicationsExamInfo:
    """
    Extract and process information from an exam document to create a CommunicationsExamInfo object.

    Args:
    case_study_path (str): The file path to the exam document.

    Returns:
    CommunicationsExamInfo: An object containing processed information from the exam document.
    """
    # Read the exam document
    case_study_info = read_docx(case_study_path)

    # Extract specific sections from the document
    candidate_task, abbreviations, email, content = case_study_extract(case_study_info)

    # Combine and process text with GPT models
    processed_candidate_task = generate_candidate_task_gpt(candidate_task + abbreviations + email)
    summary = generate_summary_gpt(content)
    point_of_views = extract_point_of_views_gpt(abbreviations + content)
    target_audience = extract_target_audience_gpt(processed_candidate_task + abbreviations + email)

    return CommunicationsExamInfo(
        summary_text=summary,
        abbreviations=abbreviations,
        points_of_view=point_of_views,
        target_audience=target_audience,
        candidate_task=candidate_task,
    )
