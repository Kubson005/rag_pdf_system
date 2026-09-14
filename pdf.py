from pypdf import PdfReader


def load_pdf(filename):
    reader = PdfReader(filename)
    num_pages = len(reader.pages)
    document = ""

    for i in range(num_pages):
        page = reader.pages[i]
        document += page.extract_text()

    return document


def chunk_text(text, chunk_size=100, overlap=20):
    chunks = []

    step = chunk_size - overlap
    for i in range(0, len(text), step):
        chunk = text[i : i + chunk_size]
        if chunk:
            chunks.append(chunk)
        if i + chunk_size >= len(text):
            break

    return chunks
