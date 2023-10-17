import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from openai_training.training_file import *
from database.schema import CaseStudy
from openai_training.finetune import generate_finetune

if __name__ == "__main__":
    # Create a parser object
    parser = argparse.ArgumentParser(description="Create Training Files")
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
        generate_training_clubbed(case_studies_id, session, summary_var)
    elif args.command == "singleton":
        generate_training_singleton(case_studies_id, session, summary_var)
    elif args.command == "clubbed_finetune":
        generate_finetune("clubbed", summary_var)
    elif args.command == "singleton_finetune":
        generate_finetune("singleton", summary_var)

    session.close()
