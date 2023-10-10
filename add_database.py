import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Base, CaseStudy, ReviewGuide, CaseStudyEvaluation

# Create a database engine (SQLite in this case)
engine = create_engine('sqlite:///eutraining.db', echo=True)

# Check if the database file exists
if not os.path.isfile('eutraining.db'):
    # Create the tables in the database
    Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Add data to the tables
try:
    # Add data to the CaseStudy table
    case_study_1 = CaseStudy(
        instructions="Sample instructions 1",
        abbreviations="Abbreviations for case study 1",
        email_instructions="Email instructions for case study 1",
        context="Context for case study 1",
        name="Case Study 1"
    )
    session.add(case_study_1)

    # Add data to the ReviewGuide table
    review_guide_1 = ReviewGuide(
        case_study_id=1,  # Assuming case_study_id 1 corresponds to Case Study 1
        recommendations="Recommendations for Case Study 1",
        score_grid="Score grid for Case Study 1"
    )
    session.add(review_guide_1)

    # Add data to the CaseStudyEvaluation table
    case_study_evaluation_1 = CaseStudyEvaluation(
        case_study_id=1,  # Assuming case_study_id 1 corresponds to Case Study 1
        overall_score=85,
        overall_summary="Overall summary for Case Study 1",
        communication_score=90,
        communication_summary="Communication summary for Case Study 1",
        communication_errors="Communication errors for Case Study 1",
        communication_tips="Communication tips for Case Study 1",
        trainee_answer="Trainee's answer for Case Study 1"
    )
    session.add(case_study_evaluation_1)

    # Commit the changes to the database
    session.commit()
    print("Data added to the database successfully.")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    session.rollback()

finally:
    # Close the session
    session.close()
