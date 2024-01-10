from schema import EvaluationRequestSchema
from evaluate import evaluate  # Import the evaluate function

def main(args: dict) -> dict:
    """ Case Study Info """
    case_study_data = EvaluationRequestSchema(**args)

    # Extract the necessary data for evaluation
    candidate_response_data = case_study_data.candidate_response  
    exam_doc_data = case_study_data.exam_doc

    # Perform the evaluation
    evaluation = evaluate(candidate_response_data, exam_doc_data)

    return {
        'body': {
            "summary": evaluation.summary,
            "score": evaluation.score,
            "observations": evaluation.observations,
            "tips": evaluation.tips           
        }
    }