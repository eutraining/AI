from apis.openai_api import call_gpt_api, call_gpt_4_1106_preview, call_gpt35_turbo
from models.models import CommunicationsExamInfo
from utils import fetch_prompt_message
from config import settings

import openai


def generate_section_gpt(
    section: str,
    candidate_response: str,
    exam_info: CommunicationsExamInfo,
    text_until_now: str,
    guideline: str,
    perfect_response: str = ""
) -> str:
    """
    Generates a specific evaluation section using GPT,

    Args:
    section (str): The name of the section to generate.
    candidate_response (str): The candidate's response text.
    exam_info (CommunicationsExamInfo): Extracted information from the exam.
    text_until_now (str): The text of the evaluation generated up to this point.
    guideline (str): Specific guidelines for generating this section.
    perfect_response (str, optional): An ideal response for comparison.

    Returns:
    str: The generated text for the specified section.
    """
    # Fetch necessary templates and context
    system_messages = fetch_prompt_message(settings.SYSTEM_MESSAGES_PATH)
    prompt_templates = fetch_prompt_message(settings.GENERAL_TEMPLATE_PATH)
    general_messages = fetch_prompt_message(settings.GENERAL_MESSAGE_PATH)
    evaluation_structure = fetch_prompt_message(settings.EVALUATION_STRUCTURE_PATH)
    user_feedback = fetch_prompt_message(settings.USER_FEDDBACK_PATH)
    tasks = fetch_prompt_message(settings.TASK_PATH)
    workflow = fetch_prompt_message(settings.WORKFLOW_PATH)
    exam_info_template = fetch_prompt_message(settings.EXAM_INFO_PATH)
    ambient_context = fetch_prompt_message(settings.AMBIENT_CONTEXT_PATH)
    role = fetch_prompt_message(settings.ROLE_PATH)

    # Fill in the exam information template
    exam_info_filled = exam_info_template.format(
        exam_summary=exam_info.summary_text,
        point_of_views=exam_info.points_of_view,
        target_audience=exam_info.target_audience,
        candidate_task=exam_info.candidate_task,
    )

    # Prepare the prompt with all necessary information
    prompt = prompt_templates.format(
        general_message=general_messages,
        evaluation_structure=evaluation_structure,
        abbreviations=exam_info.abbreviations,
        workflow=workflow,
        task=tasks,
        user_feedback=user_feedback,
        ambient_context=ambient_context,
        role=role,
        exam_info=exam_info_filled,
        candidate_response=candidate_response,
        example=perfect_response,
        evaluation_until_now=text_until_now,
        guideline=guideline,
        section=section
    )

    # Call the GPT API to generate the section text
    section_text = call_gpt_api(system_messages, prompt)
    
    return section_text


def generate_summary_gpt(evaluation_text: str) -> str:
    """
    Generates a summary of the evaluation text using GPT.

    Args:
    evaluation_text (str): The complete evaluation text that needs to be summarized.

    Returns:
    str: A concise summary preserving the core ideas and crucial details of the evaluation text.
    """
    # Fetch the summary template
    summary_template = fetch_prompt_message(settings.SUMMARY_PATH)

    # Prepare the prompt with the evaluation text
    prompt = summary_template.replace("{evaluation_text}", evaluation_text)

    # Call the GPT API to generate the summary
    summary_text = call_gpt_api("You possess excellent summarization skills, adept at condensing lengthy texts while preserving the core ideas and crucial details", prompt)

    return summary_text


def generate_candidate_task_gpt(evaluation_text: str) -> str:
    """
    Generates a description of the candidate's task based on the evaluation text.

    Args:
    evaluation_text (str): The text of the evaluation which includes details about the candidate's task.

    Returns:
    str: A generated text describing the objective or task of the candidate as interpreted from the evaluation text.
    """
    # Fetch the candidate task template
    candidate_task_template = fetch_prompt_message(settings.CANDIDATE_TASK_PATH)

    # Prepare the prompt with the evaluation text
    prompt = candidate_task_template.replace("{evaluation_text}", evaluation_text)

    # Call the GPT API to generate the candidate task description
    candidate_task_description = call_gpt_api("Your expertise lies in deciphering the underlying tasks from detailed instructions", prompt)

    return candidate_task_description


def extract_point_of_views_gpt(evaluation_text: str) -> str:
    """
    Extracts and analyzes various points of view from the evaluation text using GPT.

    Args:
    evaluation_text (str): The text of the evaluation from which different perspectives need to be identified.

    Returns:
    str: Text containing the identified and analyzed points of view.
    """
    # Fetch the views template
    views_template = fetch_prompt_message(settings.VIEWS_PATH)

    # Prepare the prompt with the evaluation text
    prompt = views_template.replace("{evaluation_text}", evaluation_text)

    # Call the GPT API to extract and analyze points of view
    views = call_gpt_api("You are a sophisticated model with the ability to discern and analyze various perspectives on the same topic", prompt)

    return views


def extract_target_audience_gpt(evaluation_text: str) -> str:
    """
    Identifies the target audience of a given evaluation text using GPT.

    Args:
    evaluation_text (str): The text of the evaluation from which the target audience needs to be determined.

    Returns:
    str: Text containing the identified target audience.
    """
    # Fetch the target audience template
    target_audience_template = fetch_prompt_message(settings.TARGET_AUDIENCE_PATH)

    # Prepare the prompt with the evaluation text
    prompt = target_audience_template.replace("{evaluation_text}", evaluation_text)

    # Call the GPT API to identify the target audience
    audience = call_gpt_api("As a highly capable model, you possess the ability to discern the target audience of a given text", prompt)

    return audience


def generate_evaluation(writing: str, abbreviations: str, prompt_path: str, gpt_model: str) -> str:
    template = fetch_prompt_message(prompt_path)
    prompt_text = template.replace("{writing}", writing)
    prompt_text = prompt_text.replace("{abbreviations}", abbreviations)
    return prompt(prompt_text, gpt_model)


def generate_initial_report(writing: str, task: str, evaluations: str, prompt_path: str, gpt_model: str) -> str:
    template = fetch_prompt_message(prompt_path)
    prompt_text = template.replace("{writing}", writing)
    prompt_text = prompt_text.replace("{task}", task)
    prompt_text = prompt_text.replace("{evaluations}", evaluations)
    return prompt(prompt_text, gpt_model)

def generate_final_report(writing: str, task: str, initial_assessment: str, prompt_path: str, gpt_model: str) -> str:
    template = fetch_prompt_message(prompt_path)
    prompt_text = template.replace("{writing}", writing)
    prompt_text = prompt_text.replace("{task}", task)
    prompt_text = prompt_text.replace("{initial_assessment}", initial_assessment)
    return prompt(prompt_text, gpt_model)


def prompt(prompt: str, model: str) -> str:
    if model == 'gpt-3.5':
        return call_gpt35_turbo('', prompt)
    else:
        return call_gpt_4_1106_preview('', prompt)
