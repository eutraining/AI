import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from training.openai_training.training_file import *
from database.schema import CaseStudy, CaseStudyEvaluation
from training.openai_training.finetune import generate_finetune, babbage_finetune, create_babbage_dataset, create_gpt_dataset, gpt_finetune_train
from config import settings


def assign_summary(arguments: argparse.Namespace) -> bool:
    if arguments.input_path == "YES":
        summary = True
    else:
        summary = False
    return summary


if __name__ == "__main__":
    # Create a parser object
    parser = argparse.ArgumentParser(description="Create Training Files")
    # Add common command-line arguments
    parser.add_argument("command", help="The command to execute (extract or update)")
    parser.add_argument("-i", "--input_path", help="Method")
    parser.add_argument("-o", "--output_path", help="Method")
    # Parse the command-line arguments
    args = parser.parse_args()

    engine = create_engine(settings.DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()

    case_studies_id = session.query(CaseStudy.case_study_id).all()
    case_studies_id = [value[0] for value in case_studies_id]

    evaluation_studies_id = session.query(CaseStudyEvaluation.case_study_evaluation_id).all()
    evaluation_studies_id = [value[0] for value in evaluation_studies_id]

    # Check the command and execute corresponding action
    if args.command == "clubbed":
        summary_var = assign_summary(args)
        generate_training_clubbed(case_studies_id, session, summary_var)
    elif args.command == "singleton":
        summary_var = assign_summary(args)
        generate_training_singleton(case_studies_id, session, summary_var)
    elif args.command == "clubbed_finetune":
        summary_var = assign_summary(args)
        generate_finetune("clubbed", summary_var)
    elif args.command == "singleton_finetune":
        summary_var = assign_summary(args)
        generate_finetune("singleton", summary_var)
    elif args.command == "train_test":
        train_validation_split(evaluation_studies_id, session)
    elif args.command == "babbage-dataset-split":
        create_babbage_dataset(args.output_path)
    elif args.command == "babbage-finetune":
        metric = args.input_path
        babbage_finetune(metric)
    elif args.command == "gpt-dataset-split":
        create_gpt_dataset(args.output_path)
    elif args.command == "gpt-finetune":
        metric = args.input_path
        gpt_finetune_train(metric)
    session.close()
