from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base

# Create an SQLite database engine. You can change the database URL to match your database type.
engine = create_engine('sqlite:///eutraining.db', echo=True)

# Create a base class for declarative models.
Base = declarative_base()


# Define the CaseStudy class to map to the 'case_study' table.
class CaseStudy(Base):
    __tablename__ = 'case_study'

    # Define columns for the 'case_study' table.
    case_study_id = Column(Integer, primary_key=True, autoincrement=True)
    instructions = Column(String, nullable=False)
    abbreviations = Column(String)
    email_instructions = Column(String, nullable=False)
    context = Column(String, nullable=False)
    name = Column(String, nullable=False)


# Define the ReviewGuide class to map to the 'review_guide' table.
class ReviewGuide(Base):
    __tablename__ = 'review_guide'

    # Define columns for the 'review_guide' table.
    case_study_id = Column(Integer, ForeignKey('case_study.case_study_id'), primary_key=True)
    recommendations = Column(String)
    score_grid = Column(String, nullable=False)


# Define the CaseStudyEvaluation class to map to the 'case_study_evaluation' table.
class CaseStudyEvaluation(Base):
    __tablename__ = 'case_study_evaluation'

    # Define columns for the 'case_study_evaluation' table.
    case_study_evaluation_id = Column(Integer, primary_key=True, autoincrement=True)
    case_study_id = Column(Integer, ForeignKey('case_study.case_study_id'), nullable=False)
    overall_score = Column(Float, nullable=False)
    overall_summary = Column(String, nullable=False)
    communication_score = Column(Float, nullable=False)
    communication_summary = Column(String)
    communication_errors = Column(String)
    communication_tips = Column(String)
    trainee_answer = Column(String, nullable=False)


if __name__ == "__main__":
    # Create the tables in the database based on the class definitions.
    Base.metadata.create_all(engine)
