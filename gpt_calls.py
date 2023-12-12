from apis.openai_api import call_gpt_api
from models.models import CommunicationsExamInfo
from utils import fetch_prompt_message
from config import settings

import openai


def generate_section_gpt(
    section: str,
    candidate_response: str,
    exam_info: CommunicationsExamInfo,
    text_until_now: str,
    guideline: str
) -> str:
    """Generates a specific evaluation section"""

    SYSTEM_MESSAGES: str = fetch_prompt_message(settings.SYSTEM_MESSAGES_PATH)

    PROMPT_TEMPLATES: str = fetch_prompt_message(settings.GENERAL_TEMPLATE_PATH)

    GENERAL_MESSAGES: str = fetch_prompt_message(settings.GENERAL_MESSAGE_PATH)

    EVALUATION_STRUCTURE: str = fetch_prompt_message(settings.EVALUATION_STRUCTURE_PATH)

    USER_FEEDBACK: str = fetch_prompt_message(settings.USER_FEDDBACK_PATH)

    TASKS: str = fetch_prompt_message(settings.TASK_PATH)

    WORKFLOW: str = fetch_prompt_message(settings.WORKFLOW_PATH)

    EXAM_INFO: str = fetch_prompt_message(settings.EXAM_INFO_PATH)

    prompt = PROMPT_TEMPLATES

    # region Add the exam info to prompt
    exam_info_filled = EXAM_INFO.replace("{exam_summary}", exam_info.summary_text)
    exam_info_filled = exam_info_filled.replace("{point_of_views}", exam_info.points_of_view)
    exam_info_filled = exam_info_filled.replace("{target_audience}", exam_info.target_audience)
    exam_info_filled = exam_info_filled.replace("{candidate_task}", exam_info.candidate_task)
    # endregion
    
    prompt = prompt.replace("{general_message}", GENERAL_MESSAGES)
    prompt = prompt.replace("{evaluation_structure}", EVALUATION_STRUCTURE)
    prompt = prompt.replace("{workflow}", WORKFLOW)
    prompt = prompt.replace("{task}", TASKS)
    prompt = prompt.replace("{user_feedback}", USER_FEEDBACK)
    prompt = prompt.replace("{exam_info}", exam_info_filled)
    prompt = prompt.replace("{abbreviations}", exam_info.abbreviations)
    prompt = prompt.replace("{candidate_response}", candidate_response)
    prompt = prompt.replace("{evaluation_until_now}", text_until_now)
    prompt = prompt.replace("{guideline}", guideline)

    # Set the actual section name
    prompt = prompt.replace("{section}", section)

    section_text = call_gpt_api(SYSTEM_MESSAGES, prompt)
    
    return section_text

def generate_summary_gpt(evaluation_text: str) -> str:
    """Generates the summary text"""

    SUMMARY: str = fetch_prompt_message(settings.SUMMARY_PATH)

    prompt = SUMMARY
    prompt = prompt.replace("{evaluation_text}", evaluation_text)

    summary_text = call_gpt_api("You possess excellent summarization skills, adept at condensing lengthy texts while preserving the core ideas and crucial details", prompt)

    return summary_text


def generate_candidate_task_gpt(evaluation_text: str) -> str:
    """Generates the summary text"""

    CANDIDATE_TASK_PATH: str = fetch_prompt_message(settings.CANDIDATE_TASK_PATH)

    prompt = CANDIDATE_TASK_PATH
    prompt = prompt.replace("{evaluation_text}", evaluation_text)

    summary_text = call_gpt_api("You are a great finding out the objective task behind various instructions", prompt)

    return summary_text

def extract_point_of_views_gpt(evaluation_text: str) -> str:
    VIEWS: str = fetch_prompt_message(settings.VIEWS_PATH)

    prompt = VIEWS
    prompt = prompt.replace("{evaluation_text}", evaluation_text)

    views = call_gpt_api("You are a sophisticated model with the ability to discern and analyze various perspectives on the same topic", prompt)

    return views

def extract_target_audience_gpt(evaluation_text: str) -> str:
    TARGET_AUDIENCE: str = fetch_prompt_message(settings.TARGET_AUDIENCE_PATH)

    prompt = TARGET_AUDIENCE
    prompt = prompt.replace("{evaluation_text}", evaluation_text)

    audience = call_gpt_api("As a highly capable model, you possess the ability to discern the target audience of a given text", prompt)

    return audience