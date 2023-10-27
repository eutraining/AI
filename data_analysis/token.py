from openai_training.finetune import read_jsonl_with_index
from evaluation_files.evaluation import num_tokens_from_string


def average_token(path: str) -> float:
    results = read_jsonl_with_index(path)
    total = 0
    token_count = 0
    for data in results:
        value = data["messages"][1]["content"]
        token_count += num_tokens_from_string(value)
        total += 1
    avg_token = round(token_count / total)
    print(f"Average Token Count (Case Study Content): {avg_token}")
    return avg_token
