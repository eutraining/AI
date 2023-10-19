import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.schema import Base
from data_analysis.db import add_extracted_info_database


if __name__ == "__main__":
    # Base Path for Case Studies Directory
    base_folder_path = "E:/Freelancing/AXEOM/Axeom_EUTraining/CS docs for AI/Generic Case Studies"
    # Create Database Engine
    engine = create_engine('sqlite:///eutraining_v2.db', echo=True)
    # If database not present in file system, then make a new one
    if not os.path.isfile('eutraining_v2.db'):
        Base.metadata.create_all(engine)
    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()
    # Function to execute the extraction and creation of records into DB
    add_extracted_info_database(base_folder_path, session)
    # Close the session after inserting data
    session.close()
