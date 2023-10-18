import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from evaluation_files.evaluation import *
from database.schema import CaseStudy

if __name__ == "__main__":
    # Create a parser object
    parser = argparse.ArgumentParser(description="Generate Evaluation Files")
    # Add common command-line arguments
    parser.add_argument("command", help="The command to execute (extract or update)")
    parser.add_argument("-i", "--input_path", help="Method")
    # Parse the command-line arguments
    args = parser.parse_args()

    engine = create_engine('sqlite:///eutraining.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    case_studies_id = session.query(CaseStudy.case_study_id).all()
    case_studies_id = [value[0] for value in case_studies_id]
    if args.input_path == "YES":
        summary_var = True
    else:
        summary_var = False
    # Check the command and execute corresponding action
    if args.command == "clubbed":
        generate_evaluation_clubbed(case_studies_id, session, summary_var)
    elif args.command == "singleton":
        generate_evaluation_singleton(case_studies_id, session, summary_var)

    session.close()
