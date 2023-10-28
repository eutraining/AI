import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from evaluation.evaluation import *
from database.schema import CaseStudy
from evaluation.test.accuracy import accuracy_csv


def assign_summary(arguments: argparse.Namespace) -> bool:
    if arguments.input_path == "YES":
        summary = True
    else:
        summary = False
    return summary


if __name__ == "__main__":
    # Create a parser object
    parser = argparse.ArgumentParser(description="Generate Evaluation Files")
    # Add common command-line arguments
    parser.add_argument("command", help="The command to execute (extract or update)")
    parser.add_argument("-i", "--input_path", help="Method")
    # Parse the command-line arguments
    args = parser.parse_args()

    engine = create_engine(settings.DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()
    case_studies_id = session.query(CaseStudy.case_study_id).all()
    case_studies_id = [value[0] for value in case_studies_id]

    # Check the command and execute corresponding action
    if args.command == "clubbed":
        summary_var = assign_summary(args)
        generate_evaluation_clubbed(case_studies_id, session, summary_var)
    elif args.command == "singleton":
        summary_var = assign_summary(args)
        generate_evaluation_singleton(case_studies_id, session, summary_var)
    elif args.command == "babbage-score":
        summary_var = assign_summary(args)
        babbage_score(case_studies_id, session, summary_var)
    elif args.command == "gpt-score":
        summary_var = assign_summary(args)
        gpt_score(case_studies_id, session, summary_var)
    elif args.command == "accuracy":
        base_path = "../training/results/singleton/summary/"
        output_path = "./evaluation/test/accuracy_score.csv"
        accuracy_csv(base_path, output_path)
    session.close()
