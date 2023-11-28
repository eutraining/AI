import csv


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


def create_score_evaluation_data(name: str, instructions: str, abbreviations: str,
                                 email_instructions: str, context: str, trainee_ans: str) -> str:
    sample_data = f"Case Study Name: \n{name}\n\n" \
                  f"Instructions/Important Notice: \n{instructions}\n\n" \
                  f"Abbreviations (if any): \n{abbreviations}\n\n" \
                  f"Email Instructions to be followed: \n{email_instructions}\n\n" \
                  f"Case Study Content: \n{context}\n\n" \
                  f"Trainee's Answer: \n{trainee_ans}\n"
    return sample_data


def create_overall_content(overall_summary: str, overall_score: float) -> str:
    data = f"Overall Score (out of 10): {overall_score}\n\n" \
           f"Overall Summary: \n{overall_summary}\n"
    return data


def create_communication_content(communication_summary: str, communication_score: float) -> str:
    data = f"Communication Score(out of 10): {communication_score}\n\n" \
           f"Communication Summary: \n{communication_summary}\n"
    return data


def create_tips_errors(tips: str, errors: str) -> str:
    data = f"Tips/Suggestions for Improvement (if any): \n{tips}\n\n" \
           f"Spelling/Grammar Errors (if any): \n{errors}\n"
    return data


def create_csv_file(data: list, filename: str) -> None:
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
