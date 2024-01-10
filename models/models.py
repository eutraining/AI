from pydantic import BaseModel

# class that represent relevant info of an exam case
class CommunicationsExamInfo(BaseModel):
    summary_text: str
    abbreviations: str
    points_of_view: str
    target_audience: str
    candidate_task: str