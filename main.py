from generate_text import generate_full_text
from process_docx import create_docx
from utils import load_doc

def evaluate(candidate_response_path: str, exam_doc_path: str, perfect_response_path: str = "") -> str:
    """
    Generate evaluation docx with the candidate_response.

    Args:
    candidate_response_path (str): Path to the candidate's response.
    exam_doc_path (str): Path to the exam document.
    perfect_response_path (str, optional): Path to the perfect response, if available.

    Returns:
    str: Path to the generated DOCX file containing the evaluation.
    """
    # Load the candidate response
    candidate_response = load_doc(candidate_response_path)

    # Load the perfect response if provided
    perfect_response = load_doc(perfect_response_path) if perfect_response_path else ""

    # Generate evaluation text
    processed_evaluation_text, summary_text = generate_full_text(candidate_response, exam_doc_path, perfect_response)

    # Create a new DOCX document
    doc = create_docx(0, summary_text, processed_evaluation_text)

    return doc


if __name__ == "__main__":
    CASE_STUDY_PATH = "" #Case study path 
    CANDIDATE_RESPONSE_PATH = "" #Response path
    evaluate(CANDIDATE_RESPONSE_PATH, CASE_STUDY_PATH)