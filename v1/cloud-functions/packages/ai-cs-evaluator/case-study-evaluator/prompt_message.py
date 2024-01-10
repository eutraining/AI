def fetch_prompt_message(filepath: str) -> str:
    with open(filepath, "r") as f:
        data = f.read()
    return data
