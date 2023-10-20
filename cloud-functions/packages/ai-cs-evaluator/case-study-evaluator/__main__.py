from evaluation import generate_evaluation
'''
Input Request Format
{
  "case_study": {
    "question": "string",
    "introduction": "string",
    "assignment": "string",
    "sample_solution": "string",
    "attachments": [
      {
        "title": "string",
        "body": "string"
      }
    ]
  },
  "trainee_answer": "string"
}
'''

'''
Output Response Format
{
  "overall_score": "string",
  "overall_summary": "string",
  "competencies": {
    "communication": {
      "score": "string",
      "observations": "string",
      "tips": "string"
    }
  }
}
'''


def main(args: dict) -> dict:
    # Get parameters from the input arguments
    """ Case Study Info """
    case_study = args.get("case_study")
    question = case_study.get("question")
    introduction = case_study.get("introduction")
    assignment = case_study.get("assignment")
    sample_solution = case_study.get("sample_solution")
    attachments = case_study.get("attachments")
    case_study_info = (question, introduction, assignment, sample_solution, attachments)
    """ Trainee's Answer"""
    trainee_answer = args.get("trainee_answer")
    score_content, summary_content, competencies = generate_evaluation(case_study_info, trainee_answer)
    # Return a response including the evaluation information
    return {'body': {
          "overall_score": score_content,
          "overall_summary": summary_content,
          "competencies": competencies
        }}
