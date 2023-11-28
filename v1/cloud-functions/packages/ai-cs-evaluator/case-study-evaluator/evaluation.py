from openai_api import call_gpt_api
from config import settings
from schema import EvaluationRequestSchema, AttachmentSchema, EvaluationResponseSchema


def create_evaluation_sample(question: str, instructions: str, assignment: str,
                             sample_solution: str, attachments: str, trainee_ans: str) -> str:
    sample_data = f"Case Study Name: \n{question}\n\n" \
                  f"Instructions: \n{instructions}\n\n" \
                  f"Assignment: \n{assignment}\n\n" \
                  f"Case Study Content: \n{attachments}\n\n" \
                  f"Trainee's Answer: \n{trainee_ans}\n" \
                  f"Sample Solution for Reference: \n{sample_solution}\n"
    return sample_data


def create_score_evaluation_data(question: str, instructions: str, assignment: str,
                                 attachments: str, trainee_ans: str) -> str:
    sample_data = f"Case Study Name: \n{question}\n\n" \
                  f"Instructions: \n{instructions}\n\n" \
                  f"Assignment: \n{assignment}\n\n" \
                  f"Case Study Content: \n{attachments}\n\n" \
                  f"Trainee's Answer: \n{trainee_ans}\n"
    return sample_data


def fetch_attachments(attachments: list[AttachmentSchema]) -> str:
    case_study_content = ""
    for attachment in attachments:
        case_study_content += f"## {attachment.title}:\n"
        case_study_content += f"{attachment.body}\n\n"
    return case_study_content


def extract_data(case_study_info: EvaluationRequestSchema) -> tuple:
    trainee_answer = case_study_info.trainee_answer
    question = case_study_info.case_study.question
    introduction = case_study_info.case_study.introduction
    assignment = case_study_info.case_study.assignment
    sample_solution = case_study_info.case_study.sample_solution
    attachments = fetch_attachments(case_study_info.case_study.attachments)
    return question, introduction, assignment, sample_solution, attachments, trainee_answer


def generate_evaluation(case_study_info: EvaluationRequestSchema) -> EvaluationResponseSchema:
    question, introduction, assignment, sample_solution, attachments, trainee_answer = extract_data(case_study_info)
    '''Summary Generation for Case Study Content'''
    attachments = call_gpt_api(settings.SUMMARY_MESSAGE, attachments)
    # Create Evaluation Sample and Other Data
    sample_evaluation_data = create_evaluation_sample(question, introduction, assignment,
                                                      sample_solution, attachments, trainee_answer)
    sample_score_data = create_score_evaluation_data(question, introduction, assignment,
                                                     attachments, trainee_answer)
    # GPT Data Fetching
    '''Competencies - Communication'''
    communication_summary_content = call_gpt_api(settings.COMMUNICATION_SUMMARY_MESSAGE, sample_evaluation_data)
    communication_score_content = call_gpt_api(settings.COMMUNICATION_SCORE_MESSAGE,
                                               sample_score_data,
                                               model="ft:gpt-3.5-turbo-0613:eu-training::8DpWReUf")
    '''Overall Summary'''
    summary_content = call_gpt_api(settings.OVERALL_SUMMARY_MESSAGE, sample_evaluation_data)
    '''Overall Score'''
    score_content = call_gpt_api(settings.OVERALL_SCORE_MESSAGE, sample_score_data,
                                 model="ft:gpt-3.5-turbo-0613:eu-training::8Dp8J3iS")
    '''Tips/Errors'''
    tips_errors = call_gpt_api(settings.TIPS_ERRORS_MESSAGE, sample_evaluation_data)
    ''''''
    response_data = {
        "overall_score": score_content,
        "overall_summary": summary_content,
        "competencies": {
            "communication": {
                "score": communication_score_content,
                "observations": communication_summary_content,
                "tips": tips_errors
            }
        }
    }
    response_object = EvaluationResponseSchema(**response_data)
    return response_object
