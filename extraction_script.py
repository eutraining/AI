import docx
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
import re


def read_docx(docx_path):
    doc = docx.Document(docx_path)
    document_text = ""
    document_paragraph = doc.paragraphs
    document_table = doc.tables
    body_location = []
    for element in doc.element.body:
        if isinstance(element, CT_Tbl):
            body_location.append("T")
        elif isinstance(element, CT_P):
            body_location.append("P")
    para, tab = 0, 0
    for loc in body_location:
        if loc == "P":
            document_text += document_paragraph[para].text + "\n"
            para += 1
        elif loc == "T":
            for row in document_table[tab].rows:
                row_text = ""
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        paragraph_text = paragraph.text
                        row_text += paragraph_text + " | "
                document_text += row_text.strip() + "\n"
            tab += 1
    document_text = document_text.strip()
    return document_text


def trainee_answer_extractor(trainee_answer):
    question_start = trainee_answer.find("Question")
    trainee_answer_start = trainee_answer.find("Trainee's Answer")
    case_study_name = trainee_answer[question_start:trainee_answer_start].strip()
    answer_content = trainee_answer[trainee_answer_start:].strip()
    return case_study_name, answer_content


def review_guide_extract(review_info):
    pattern = r"Communication[\s\S]+?Key tips to improve / maintain performance:"
    communication_section = re.search(pattern, review_info)
    if communication_section is not None:
        return communication_section.group(0)

