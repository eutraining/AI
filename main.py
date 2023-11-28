def evaluate(candidate_response: str, exam_case: ExamCase):
    """Generates the evaluation text and the summary text"""
    
    # preprocess necessary information
    # method for get all the info from exam

    # generate evaluation text
    processed_evaluation_text, summary_text, score = generate_full_text(candidate_response, *args)

    # generate score (not implemented yet)
    #score = generate_score(processed_evaluation_text)  

    doc = create_docx(score, summary_text, processed_evaluation_text)

    return doc