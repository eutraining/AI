from pydantic import BaseModel


class AttachmentSchema(BaseModel):
    title: str
    body: str


class CaseStudySchema(BaseModel):
    question: str
    introduction: str
    assignment: str
    sample_solution: str
    attachments: list[AttachmentSchema]


class EvaluationRequestSchema(BaseModel):
    case_study: CaseStudySchema
    trainee_answer: str


class Competency(BaseModel):
    score: str
    observations: str
    tips: str


class EvaluationResponseSchema(BaseModel):
    overall_score: str
    overall_summary: str
    competencies: dict[str, Competency]
