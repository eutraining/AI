from openai_api import call_gpt_api
from config import settings


def generate_summary(instructions: str, email: str, content: str) -> tuple:
    instructions = call_gpt_api(settings.SUMMARY_MESSAGE, instructions)
    email = call_gpt_api(settings.SUMMARY_MESSAGE, email)
    content = call_gpt_api(settings.SUMMARY_MESSAGE, content)
    return instructions, email, content


def add_summary(sample_evaluation: str, summary: str, metric: str) -> str:
    metric_data = f"\n\n{metric} Summary Feedback: \n{summary}\n"
    data = sample_evaluation + metric_data
    return data


def add_score(evaluation_data: str, score: str, metric: str) -> str:
    metric_data = f"\n\n{metric} Score Feedback: \n{score}"
    data = evaluation_data + metric_data
    return data


def create_evaluation_sample(question: str, instructions: str, assignment: str,
                             sample_solution: str, attachments: str, trainee_ans: str) -> str:
    sample_data = f"Case Study Name: \n{question}\n\n" \
                  f"Instructions: \n{instructions}\n\n" \
                  f"Assignment: \n{assignment}\n\n" \
                  f"Case Study Content: \n{attachments}\n\n" \
                  f"Trainee's Answer: \n{trainee_ans}\n" \
                  f"Sample Solution for Reference: \n{sample_solution}\n"
    return sample_data


def generate_evaluation(case_study_info: tuple, trainee_answer: str) -> tuple:
    question, introduction, assignment, sample_solution, attachments = case_study_info
    # Create Evaluation Sample and Other Data
    sample_evaluation_data = create_evaluation_sample(question, introduction, assignment,
                                                      sample_solution, attachments, trainee_answer)
    # GPT Data Fetching
    '''Competencies - Communication'''
    communication_summary_content = call_gpt_api(settings.COMMUNICATION_SUMMARY_MESSAGE, sample_evaluation_data)
    communication_score_evaluation = add_summary(sample_evaluation_data, communication_summary_content,
                                                 "Communication")
    communication_score_content = call_gpt_api(settings.COMMUNICATION_SCORE_MESSAGE,
                                               communication_score_evaluation)
    '''Overall Summary'''
    summary_content = call_gpt_api(settings.OVERALL_SUMMARY_MESSAGE, sample_evaluation_data)
    '''Overall Score'''
    score_evaluation = add_summary(sample_evaluation_data, summary_content, "Overall")

    score_content = call_gpt_api(settings.OVERALL_SCORE_MESSAGE, score_evaluation)
    '''Tips/Errors'''
    tips_errors = call_gpt_api(settings.TIPS_ERRORS_MESSAGE, sample_evaluation_data)
    '''Join Competencies'''
    competencies = {
        "communication": {
            "score": communication_score_content,
            "observations": communication_summary_content,
            "tips": tips_errors
        }
    }
    ''''''
    return score_content, summary_content, competencies







