from src.Parse.ImageParser import ImageParser
from src.Parse.PDFParser import PDFParser


class ParserController():
    instance = None

    @classmethod
    def get_one(cls):
        if cls.instance is None:
            cls.instance = ParserController()
        return cls.instance

    def parse(self, file):
        if file.mimetype == "application/pdf":
            return PDFParser(file.read()).parse()
        elif file.mimetype.startswith("image"):
            return ImageParser(file).parse()
        raise Exception("Unsupported file type")
