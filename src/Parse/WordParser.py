from io import BytesIO
from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE
import re

class WordParser():
    def __init__(self, blob: bytearray):
        self.docx_bytes = BytesIO(blob)
        self.doc = Document(self.docx_bytes)
        return
    
    def ensure_https(self, url):
        # regex checks if URL starts with http:// or https://
        if not re.match(r'^https?:\/\/', url):
            url = 'https://' + url
            return url
        return url
        
    def parse(self):
        text = ""
        hyperlinks = []
        for paragraph in self.doc.paragraphs:
            text += paragraph.text + "\n"

        rels = self.doc.part.rels
        for rel in rels:
            if rels[rel].reltype == RELATIONSHIP_TYPE.HYPERLINK:
                corrected_url = self.ensure_https(rels[rel]._target)
                hyperlinks.append(corrected_url)

        return text + "\n".join(hyperlinks)


