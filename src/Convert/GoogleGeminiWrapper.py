

import json
import os
import requests


URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key="

class GoogleGenimiWrapper():
    gemini_client = None

    @classmethod
    def get_one(cls):
        if cls.gemini_client is None:
            cls.gemini_client = GoogleGenimiWrapper()
            cls.gemini_client.prompt = open("Convert/prompt.txt", "r").read()
            cls.gemini_client.structure = open("Convert/structure.json", "r").read()
        return cls.gemini_client
    
    def format_text(self, text):
        key =  os.environ['GEMINI_API_KEY']
        data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": self.prompt + self.structure + text
                    }
                ]
            }
        ]
        }

        headers = {
            "Content-Type": "application/json"
        }


        response = requests.post(URL + key, headers=headers, json=data)
        data = response.json()['candidates'][0]['content']['parts'][0]['text']
        print(data)
        return json.loads(data)
    

