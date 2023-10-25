import json
from chatgpt_api.config import settings


def create_evaluation_sample(name: str, instructions: str, abbreviations: str,
                             email_instructions: str, context: str, trainee_ans: str, sample_solution: str) -> str:
    sample_data = f"Case Study Name: \n{name}\n\n" \
                  f"Instructions/Important Notice: \n{instructions}\n\n" \
                  f"Abbreviations (if any): \n{abbreviations}\n\n" \
                  f"Email Instructions to be followed: \n{email_instructions}\n\n" \
                  f"Case Study Content: \n{context}\n\n" \
                  f"Sample Referenced Solution: \n{sample_solution}\n\n" \
                  f"Trainee's Answer: \n{trainee_ans}\n"
    return sample_data


def create_overall_content(overall_summary: str, overall_score: float) -> str:
    data = f"Overall Score (out-off 10): {overall_score}\n\n" \
           f"Overall Summary: \n{overall_summary}\n"
    return data


def create_score_content(metric: str, score: float) -> str:
    data = f"{metric} Score (out-off 10): {score}\n\n"
    return data


def create_summary_content(metric: str, summary: str) -> str:
    data = f"{metric} Summary: \n{summary}\n"
    return data


def create_communication_content(communication_summary: str, communication_score: float) -> str:
    data = f"Communication Score(out-off 10): {communication_score}\n\n" \
           f"Communication Summary: \n{communication_summary}\n"
    return data


def create_tips_errors(tips: str, errors: str) -> str:
    data = f"Tips/Suggestions for Improvement (if any): \n{tips}\n\n" \
           f"Spelling/Grammar Errors (if any): \n{errors}\n"
    return data


def create_tips_errors_content(user_content: str, tips_errors_content: str) -> dict:
    return {"messages": [{"role": "system", "content": settings.TIPS_ERRORS_MESSAGE},
                         {"role": "user", "content": user_content},
                         {"role": "assistant", "content": tips_errors_content}
                         ]}


def create_overall_score(user_content: str, overall_content: str) -> dict:
    return {"messages": [{"role": "system", "content": settings.OVERALL_SCORE_SUMMARY_MESSAGE},
                         {"role": "user", "content": user_content},
                         {"role": "assistant", "content": overall_content}
                         ]}


def create_communication_score(user_content: str, communication_content: str) -> dict:
    return {"messages": [{"role": "system", "content": settings.COMMUNICATION_SCORE_SUMMARY_MESSAGE},
                         {"role": "user", "content": user_content},
                         {"role": "assistant", "content": communication_content}
                         ]}


def create_dict_data(system_message: str, user_content: str, content: str) -> dict:
    return {"messages": [{"role": "system", "content": system_message},
                         {"role": "user", "content": user_content},
                         {"role": "assistant", "content": content}
                         ]}


def create_jsonl_file(data: list, filename: str) -> None:
    with open(filename, 'w') as jsonl_file:
        for record in data:
            json_record = json.dumps(record)
            jsonl_file.write(json_record + '\n')
