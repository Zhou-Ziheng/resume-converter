import fitz
from Parse.ImageToText import ImageToText
from PIL import Image

class PDFParser():
    def __init__(self, pdf: bytearray):
        self.pdf = pdf
        return
    
    def parse(self) -> str:
        if self.pdf is None:
            raise ValueError("PDF is None")
        
        if self.is_scanned_pdf():
            return self.extract_text_from_ocr()
        else:
            return self.extract_text_from_pdf()
        
    def calculate_dpi(self, font_size_pt, page_width_in, page_height_in):
        # Calculate the DPI based on font size and page dimensions
        dpi = int(max(page_width_in, page_height_in) / font_size_pt)
        return dpi

    def extract_text_from_ocr(self) -> str:
        text = ""
        dpi = self.calculate_dpi(1, 8.5, 11)
        with fitz.open(stream=self.pdf, filetype="pdf") as doc:
            for page_number in range(len(doc)):
                page = doc.load_page(page_number)
                pix = page.get_pixmap(matrix=fitz.Matrix(1, 1).prescale(dpi, dpi))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text += ImageToText.get_text(img)
        return text
    
    def extract_text_from_pdf(self) -> str:
        text = ""
        with fitz.open(stream=self.pdf, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
    
    def is_scanned_pdf(self) -> bool:
        with fitz.open(stream=self.pdf, filetype="pdf") as doc:
            for page_number in range(len(doc)):
                page = doc.load_page(page_number)
                if len(page.get_text()) == 0:
                    return True
        return False

    
    def get_text_percentage(self) -> float:
        """
        Calculate the percentage of document that is covered by (searchable) text.

        If the returned percentage of text is very low, the document is
        most likely a scanned PDF
        """
        total_page_area = 0.0
        total_text_area = 0.0

        doc = fitz.open(stream=self.pdf, filetype="pdf")

        for page_num, page in enumerate(doc):
            total_page_area = total_page_area + abs(page.rect)
            text_area = 0.0
            for b in page.get_text_blocks():
                r = fitz.Rect(b[:4])  # rectangle where block text appears
                text_area = text_area + abs(r)
            total_text_area = total_text_area + text_area
        doc.close()
        return total_text_area / total_page_area

