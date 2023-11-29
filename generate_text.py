from gpt_calls import generate_section_gpt, generate_summary_gpt

class Sections(Enum):
    OBSERVATIONS = "Key Observations"
    GRAMMAR = "Grammar Errors"
    TIPS = "Key tips to improve"


def generate_full_text(candidate_response: str, exam_doc_path: str) -> str:
    """Generates the evaluation text and the summary text"""

    # get abbrev and candidate task -> get_exam_info(exam_doc_path)
    exam_info = get_exam_info(exam_doc_path)
 
    # generate evaluation text
    evaluation_text = generate_evaluation_text(candidate_response, exam_info)

    # generate summary text
    summary_text = generate_summary_gpt(evaluation_text)

    return processed_evaluation_text, summary_text


def generate_evaluation_text(candidate_response: str, exam_info: CommunicationsExamInfo):
    """Generates all sections of the evaluation text"""

    text_until_now = ""

    # 1. Generate observations section
    OBSERVATIONS_GUIDELLINE: str = fetch_prompt_message(settings.OBSERVATIONS_GUIDELLINE_PATH)

    observations = generate_section_gpt(
        Sections.OBSERVATIONS.value, candidate_response, exam_info, text_until_now, OBSERVATIONS_GUIDELLINE
    )

    text_until_now = observations + "\n\n"

    # 2. Generate grammar section
    GRAMMAR_GUIDELINE: str = fetch_prompt_message(settings.GRAMMAR_GUIDELINE_PATH)

    grammar = generate_section_gpt(
        Sections.GRAMMAR.value, candidate_response, exam_info, text_until_now, GRAMMAR_GUIDELINE
    )

    text_until_now = text_until_now + grammar + "\n\n"

    # 3. Generate tips section
    TIPS_GUIDELINE: str = fetch_prompt_message(settings.TIPS_GUIDELINE_PATH)

    tips = generate_section_gpt(
        Sections.TIPS.value, candidate_response, exam_info, text_until_now, TIPS_GUIDELINE
    )

    text_until_now = text_until_now + tips + "\n\n"

    # Add titles just for testing
    #observations = "Observations\n" + observations
    #grammar = "Grammar\n" + grammar
    #tips = "Tips\n" + tips

    return text_until_now


def get_exam_info(exam_doc_path: str) -> CommunicationsExamInfo:
    """Get all the info from the exam document"""
    exam_info = CommunicationsExamInfo()
    #TODO
    # charge docx

    # extract abbreviations and candidate task
    # add to exam_info fiels

    # call gpt to summarize the exam
    # add to exam_info summary_text

    # call gpt to get the points of view
    # add to exam_info points_of_view

    # call gpt to get the target audience
    # add to exam_info target_audience

    # call gpt to get the candidate task
    # add to exam_info candidate_task

    return exam_info