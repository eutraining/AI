import docx
import os

# function to create a docx file 
def create_docx(score: int, summary_text: str, evaluation_text: str):
    # Create a new document
    doc = docx.Document()

    # Add content to the document (e.g., score, summary, evaluation text)
    doc.add_heading('Evaluation Report', 0)  # Add a heading
    doc.add_paragraph(f'Score: {score}')
    doc.add_paragraph('Summary:')
    doc.add_paragraph(summary_text + "\n\n")
    doc.add_paragraph(evaluation_text)

    file_name = get_next_available_filename('evaluation_report.docx')

    # Save the document to a file
    doc.save(file_name)

def get_next_available_filename(base_filename):
    base, extension = os.path.splitext(base_filename)
    count = 1

    while os.path.exists(f"{base}_{count}{extension}"):
        count += 1

    next_filename = f"{base}_{count}{extension}"

    return next_filename
