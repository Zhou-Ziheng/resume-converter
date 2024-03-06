from io import BytesIO

class TxtParser():
    def __init__(self, blob: bytearray):
        self.txt_bytes = blob
        return
    
    def parse(self):
        return self.txt_bytes.decode('utf-8')


