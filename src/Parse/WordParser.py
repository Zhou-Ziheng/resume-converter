from io import BytesIO
from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE
import re

class WordParser():
    def __init__(self, blob: bytearray):
        self.docx_bytes = BytesIO(blob)
        self.doc = Document(self.docx_bytes)
        return
    
    def parse(self):
        text = ""
        hyperlinks = []
        for paragraph in self.doc.paragraphs:
            text += paragraph.text + "\n"

        rels = self.doc.part.rels
        for rel in rels:
            if rels[rel].reltype == RELATIONSHIP_TYPE.HYPERLINK:
                hyperlinks.append(rels[rel]._target)

        return text + "\n".join(hyperlinks)


