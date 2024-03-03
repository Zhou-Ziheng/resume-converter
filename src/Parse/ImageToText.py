import pytesseract

class ImageToText():
    def get_text(image):
        return pytesseract.image_to_string(image)