import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from chatgpt_api.config import settings
from ai_evaluation.csv_docx_data import evaluation_csv_docx

if __name__ == "__main__":
    # Create a parser object
    parser = argparse.ArgumentParser(description="Generate Client Evaluation Files DOCX/CSV")
    # Add common command-line arguments
    parser.add_argument("command", help="The command to execute (extract or update)")
    parser.add_argument("-i", "--input_path", help="Method")
    # Parse the command-line arguments
    args = parser.parse_args()

    output_path = "./ai_evaluation/evaluation.csv"
    # Create Database Engine
    engine = create_engine(settings.DB_PATH, echo=True)
    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    if args.command == "csv-output":
        evaluation_csv_docx.create_evaluation_csv(output_path, session)
    elif args.command == "docx-output":
        evaluation_csv_docx.create_docx(session)

    # Close the session after inserting data
    session.close()
