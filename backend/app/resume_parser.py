import fitz

def extract_text_from_pdf(pdf_file):

    document = fitz.open(stream=pdf_file, filetype="pdf")

    extracted_text = ""

    for page in document:
        extracted_text += page.get_text() + "\n"

    document.close()

    return extracted_text