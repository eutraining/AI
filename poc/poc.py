import json
from evaluate import generate_evaluation_text, EvaluationResult, initial_report, final_report
from generate_text import get_exam_info
from process_docx import create_docx
from utils import load_doc
from typing import List

def evaluate(candidate_response_path: str, exam_doc_path: str) -> str:
    writing = load_doc(candidate_response_path)

    exam_info = get_exam_info()
    evals = generate_evaluation_text(writing, exam_info.abbreviations)
    evals = combine_evaluation_results(evals)
    initial = initial_report(writing, exam_info.candidate_task, evals)
    final = final_report(writing, exam_info.candidate_task,initial)

    data = json.loads(clean_json_string(final))
    score = data['score']
    summary_text = data['summary']
    processed_evaluation_text = "\n\n".join([f"{eval['criteria']}\n\n{eval['assessment']}" for eval in data['evaluation']])
    # Create a new DOCX document
    create_docx(score, summary_text, processed_evaluation_text)

def clean_json_string(s: str) -> str:
    # Check if the string starts with ```json and ends with ```
    if s.startswith("```json") and s.endswith("```"):
        # Remove the markers
        s = s[len("```json"):].rstrip("```").strip()
    return s

def combine_evaluation_results(evaluation_results: List[EvaluationResult]) -> str:
    combined_evaluations = ""

    for result in evaluation_results:
        combined_evaluations += str(result) + "\n"

    return combined_evaluations.strip()


if __name__ == "__main__":
    CASE_STUDY_PATH = ''  #Case study path
    CANDIDATE_RESPONSE_PATH = ''  #Response path
    evaluate(CANDIDATE_RESPONSE_PATH, CASE_STUDY_PATH)