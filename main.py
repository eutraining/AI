from generate_text import generate_full_text
from process_docx import create_docx
import docx

def evaluate(candidate_response_path: str, exam_doc_path: str):
    
    # Load the cadidate_response
    doc = docx.Document(cadidate_response)

    candidate_response = ""

    # Iterate through all the paragraphs in the document
    for paragraph in doc.paragraphs:
        candidate_response += paragraph.text + "\n"  

    # generate evaluation text
    processed_evaluation_text, summary_text = generate_full_text(candidate_response, exam_doc_path)

    # Crear un nuevo documento DOCX
    doc = create_docx(0, summary_text, processed_evaluation_text)

    return doc

case_study = "/home/sheyla/work/ax16-eutraining/test_cases/0_Case Study Driverless Cars.docx"
cadidate_response = "/home/sheyla/work/ax16-eutraining/test_cases/driverless_cars_2.docx"
evaluate(cadidate_response, case_study)

