import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from gpt_calls import generate_evaluation, generate_initial_report, generate_final_report


class EvaluationResult:
    def __init__(self, evaluations: List[dict], score: int, overall_comments: str):
        self.evaluations = evaluations
        self.score = score
        self.overall_comments = overall_comments

## TODO: note, this is a quick PoC that I was running locally, eval directory pathes might not work properly, adjust it to your needs or generic path.
## In case something is not clear email me to ivan.nikolaichuk@inksfotware.house
def generate_evaluation_text(writing: str, abbreviations:str) -> List[EvaluationResult]:
    eval_directory = '/prompts/poc/eval'
    gpt_model = 'gpt-3.5'

    # Store future objects along with the corresponding prompt path
    future_to_prompt = {}
    results = []

    # Use ThreadPoolExecutor to execute generate function in parallel
    with ThreadPoolExecutor() as executor:
        for filename in os.listdir(eval_directory):
            if filename.endswith('.txt'):
                prompt_path = os.path.join(eval_directory, filename)

                future = executor.submit(generate_evaluation, writing, abbreviations, prompt_path, gpt_model)
                future_to_prompt[future] = prompt_path

        # Process the results as they are completed
        for future in as_completed(future_to_prompt):
            result = future.result()
            results.append(result)

    return results


def initial_report(writing: str, task: str, evals: str) -> str:
    return generate_initial_report(writing, task, evals, prompt_path('REPORT_INITIAL.txt'), 'gpt-4')

def final_report(writing: str, task: str, initial_assessment: str) -> str:
    return generate_final_report(writing, task, initial_assessment, prompt_path('REPORT_FINAL.txt'), 'gpt-4')

def prompt_path(name):
    return '/prompts/poc/eval/report/' + name


