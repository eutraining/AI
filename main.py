from generate_text import generate_full_text
from process_docx import create_docx
from utils import load_doc

def evaluate(candidate_response_path: str, exam_doc_path: str, perfect_response_path: str = ""):
    
    # Load the cadidate_response
    candidate_response = load_doc(candidate_response_path)

    perfect_response = load_doc(perfect_response_path) if perfect_response_path else ""

    # generate evaluation text
    processed_evaluation_text, summary_text = generate_full_text(candidate_response, exam_doc_path, perfect_response)

    # Crear un nuevo documento DOCX
    doc = create_docx(0, summary_text, processed_evaluation_text)

    return doc

case_study = "/home/sheyla/work/ax16-eutraining/test_cases/0_Case Study Driverless Cars.docx"
perfect_response = "/home/sheyla/work/ax16-eutraining/test_cases/driverless_car_response.docx"
cadidate_response = "/home/sheyla/work/ax16-eutraining/test_cases/driverless_cars_4.docx"
evaluate(cadidate_response, case_study)

