from gen_text import generate_full_text
from schema import EvaluationResponseSchema
#from process_docx import create_docx

import docx

def evaluate(candidate_response_path: str, exam_doc_path: str) -> EvaluationResponseSchema:
    
    # Load the cadidate_response
    doc = docx.Document(cadidate_response)

    candidate_response = ""

    # Iterate through all the paragraphs in the document
    for paragraph in doc.paragraphs:
        candidate_response += paragraph.text + "\n"  

    # generate evaluation text
    summary_text, observations, tips = generate_full_text(candidate_response, exam_doc_path)

    # Crear un nuevo documento DOCX
    #doc = create_docx(0, summary_text, processed_evaluation_text)

    return EvaluationResponseSchema(
        summary=summary_text,
        score=0,
        observations=observations,
        tips=tips
    )