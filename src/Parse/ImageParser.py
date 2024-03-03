import pytesseract
from Parse.ImageToText import ImageToText
from PIL import Image

class ImageParser():
    def __init__(self, image):
        self.image = Image.open(image)
        return
    
    def parse(self):
        return ImageToText.get_text(self.image)


