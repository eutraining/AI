from evaluation import generate_evaluation
from schema import EvaluationRequestSchema


def main(args: dict) -> dict:
    """ Case Study Info """
    case_study_data = EvaluationRequestSchema(**args)
    """Evaluation Data Info"""
    response_data = generate_evaluation(case_study_data)
    return {'body': {
          "overall_score": response_data.overall_score,
          "overall_summary": response_data.overall_summary,
          "competencies": {
              "communication": {
                  "score": response_data.competencies.get("communication").score,
                  "observations": response_data.competencies.get("communication").observations,
                  "tips": response_data.competencies.get("communication").tips
              }
          }
        }}
