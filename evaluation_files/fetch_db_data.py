from sqlalchemy.orm import Session
from data_analysis.schema import CaseStudy, CaseStudyEvaluation


def fetch_case_study(cs_id: int, session: Session) -> tuple:
    record = session.get(CaseStudy, cs_id)
    if record is not None:
        instructions = record.instructions
        abbreviations = record.abbreviations
        email_instructions = record.email_instructions
        context = record.context
        name = record.name
        return name, instructions, abbreviations, email_instructions, context


def fetch_case_study_evaluation(cs_id: int, session: Session) -> list:
    all_records = session.query(CaseStudyEvaluation).filter(CaseStudyEvaluation.case_study_id == cs_id).all()
    records_list = []
    for record in all_records:
        eval_id = record.case_study_evaluation_id
        overall_score = record.overall_score
        overall_summary = record.overall_summary
        communication_score = record.communication_score
        communication_summary = record.communication_summary
        communication_errors = record.communication_errors
        communication_tips = record.communication_tips
        trainee_answer = record.trainee_answer
        records_list.append(
            [eval_id, overall_score, overall_summary, communication_score, communication_summary, communication_errors,
             communication_tips, trainee_answer])
    return records_list
