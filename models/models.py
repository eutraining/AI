from models.base import Base

# class that represent relevant info of an exam case
class CommunicationsExamInfo(Base):
    summary_text: str
    abbreviations: str
    points_of_view: str
    target_audience: str
    candidate_task: str