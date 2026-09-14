from pypdf import PdfReader

def load_pdf(filename):
    reader = PdfReader(filename)
    num_pages = len(reader.pages)
    document = ""

    for i in range(num_pages):
        page = reader.pages[i]
        document += page.extract_text()

    return document

def chunk_text(text, chunk_size=500, imposition=50):
    chunks = []
    size = len(text)

    for i in range(0, size, chunk_size):
        if i == 0:
            chunks.append(text[i:i + chunk_size + imposition])
        elif i == size:
            chunks.append(text[i - imposition:i + chunk_size])
        else:
            chunks.append(text[i - imposition:i + chunk_size + imposition])

    return chunks

text = load_pdf("file.pdf")

chunks = chunk_text(text)

print(chunks[0])
print(chunks[1])