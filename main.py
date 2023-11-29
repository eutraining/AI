from .generate_text import generate_full_text

def evaluate(candidate_response: str, exam_doc_path: str):
    """Generates the evaluation text and the summary text"""

    # generate evaluation text
    processed_evaluation_text, summary_text, score = generate_full_text(candidate_response, exam_doc_path)

    # generate score (not needed yet)
    # score = generate_score(processed_evaluation_text)  

    doc = create_docx(score, summary_text, processed_evaluation_text)

    return doc
