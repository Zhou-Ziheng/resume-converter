from io import BytesIO
from docx import Document

class WordParser():
    def __init__(self, blob: bytearray):
        self.docx_bytes = BytesIO(blob)
        self.doc = Document(self.docx_bytes)
        return
    
    def parse(self):
        text = ""
        for paragraph in self.doc.paragraphs:
            text += paragraph.text + "\n"
        print(text)
        return text


