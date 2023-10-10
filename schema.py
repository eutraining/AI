from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base


# Create a database engine (SQLite in this case)
engine = create_engine('sqlite:///eutraining.db', echo=True)

Base = declarative_base()


class CaseStudy(Base):
    __tablename__ = 'case_study'

    case_study_id = Column(Integer, primary_key=True, autoincrement=True)
    instructions = Column(String, nullable=False)
    abbreviations = Column(String)
    email_instructions = Column(String, nullable=False)
    context = Column(String, nullable=False)
    name = Column(String, nullable=False)


# Define the Course class
class ReviewGuide(Base):
    __tablename__ = 'review_guide'

    case_study_id = Column(Integer, ForeignKey('case_study.case_study_id'), primary_key=True)
    recommendations = Column(String)
    score_grid = Column(String, nullable=False)


class CaseStudyEvaluation(Base):
    __tablename__ = 'case_study_evaluation'

    case_study_evaluation_id = Column(Integer, primary_key=True, autoincrement=True)
    case_study_id = Column(Integer, ForeignKey('case_study.case_study_id'), nullable=False)
    overall_score = Column(Integer, nullable=False)
    overall_summary = Column(String, nullable=False)
    communication_score = Column(Integer, nullable=False)
    communication_summary = Column(String)
    communication_errors = Column(String)
    communication_tips = Column(String)
    trainee_answer = Column(String, nullable=False)


if __name__ == "__main__":
    # Create the tables in the database
    Base.metadata.create_all(engine)
