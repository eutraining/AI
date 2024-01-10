from pydantic import BaseModel

# class that represent relevant info of an exam case
class CommunicationsExamInfo(BaseModel):
    summary_text: str
    abbreviations: str
    points_of_view: str
    target_audience: str
    candidate_task: str


class EvaluationRequestSchema(BaseModel):
    case_study: str
    trainee_answer: str


class EvaluationResponseSchema(BaseModel):
    summary: str
    score: int
    observations: str
    tips: str