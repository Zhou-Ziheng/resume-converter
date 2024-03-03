from Parse.ImageParser import ImageParser
from Parse.PDFParser import PDFParser


class ParserController():
    instance = None

    @classmethod
    def get_one(cls):
        if cls.instance is None:
            cls.instance = ParserController()
        return cls.instance

    def parse(self, file):
        if file.name.endswith(".pdf"):
            return PDFParser(file.read()).parse()
        elif file.name.endswith(".jpg") or file.name.endswith(".jpeg") or file.name.endswith(".png"):
            return ImageParser(file).parse()
        raise Exception("Unsupported file type")
