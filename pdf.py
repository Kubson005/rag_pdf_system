from pypdf import PdfReader


def load_pdf(filename):
    reader = PdfReader(filename)
    num_pages = len(reader.pages)
    document = ""

    for i in range(num_pages):
        page = reader.pages[i]
        document += page.extract_text()

    return document
