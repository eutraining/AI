from prompting import generate_section_gpt, generate_summary_gpt

class Sections(Enum):
    OBSERVATIONS = "Key Observations"
    GRAMMAR = "Grammar Errors"
    TIPS = "Key tips to improve"


#TODO check what args are needed
def generate_full_text(candidate_response: str, abbreviations: str, *args):
    """Generates the evaluation text and the summary text"""

    # generate evaluation text
    evaluation_text = generate_evaluation_text(candidate_response, abbreviations, *args)

    # generate summary text
    summary_text = generate_summary_gpt(evaluation_text)

    return processed_evaluation_text, summary_text


def generate_evaluation_text(candidate_response, abbreviations, *args):
    """Generates all sections of the evaluation text"""

    text_until_now = ""

    # 1. Generate observations section
    OBSERVATIONS_GUIDELLINE: str = fetch_prompt_message(settings.OBSERVATIONS_GUIDELLINE_PATH)

    observations = await generate_section_gpt(
        Sections.OBSERVATIONS.value, abbreviations, candidate_response, text_until_now, OBSERVATIONS_GUIDELLINE
    )

    text_until_now = observations + "\n\n"

    # 2. Generate grammar section
    GRAMMAR_GUIDELINE: str = fetch_prompt_message(settings.GRAMMAR_GUIDELINE_PATH)

    grammar = await generate_section_gpt(
        Sections.GRAMMAR.value, abbreviations, candidate_response, text_until_now, GRAMMAR_GUIDELINE
    )

    text_until_now = text_until_now + grammar + "\n\n"

    # 3. Generate tips section
    TIPS_GUIDELINE: str = fetch_prompt_message(settings.TIPS_GUIDELINE_PATH)

    tips = await generate_section_gpt(
        Sections.TIPS.value, abbreviations, candidate_response, text_until_now, TIPS_GUIDELINE
    )

    text_until_now = text_until_now + tips + "\n\n"

    # Add titles just for testing
    #observations = "Observations\n" + observations
    #grammar = "Grammar\n" + grammar
    #tips = "Tips\n" + tips

    return text_until_now
