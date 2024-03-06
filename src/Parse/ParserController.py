from src.Parse.ImageParser import ImageParser
from src.Parse.PDFParser import PDFParser
from src.Parse.TxtParser import TxtParser
from src.Parse.WordParser import WordParser


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
        elif file.mimetype == "application/msword" or file.mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return WordParser(file.read()).parse()
        elif file.mimetype == "text/plain":
            return TxtParser(file.read()).parse()
        raise Exception("Unsupported file type", file.mimetype)
