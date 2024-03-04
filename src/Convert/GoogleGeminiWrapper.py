

import json
import os
import time
import requests


URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key="

class GoogleGenimiWrapper():
    gemini_client = None

    @classmethod
    def get_one(cls):
        if cls.gemini_client is None:
            cls.gemini_client = GoogleGenimiWrapper()
            cls.gemini_client.prompt = open("src/Convert/prompt.txt", "r").read()
            cls.gemini_client.structure = open("src/Convert/structure.json", "r").read()
        return cls.gemini_client
    
    def process_request(self, URL, key, headers, data, app):
        retries = 2  # Number of retries
        for attempt in range(retries):
            try:
                # Send POST request
                response = requests.post(URL + key, headers=headers, json=data)
                response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
                data = response.json()['candidates'][0]['content']['parts'][0]['text']
                print(data)
                parsed_data = json.loads(data)
                return parsed_data  # Return parsed data if successful
            except (requests.RequestException, KeyError, IndexError, json.JSONDecodeError) as e:
                app.logger.error(f"Error processing request: {e}")
                if attempt < retries - 1:
                    app.logger.info("Retrying...")
                    time.sleep(1)  # Wait before retrying
                else:
                    app.logger.error("All retries failed.")
                    return None  # Return None if all retries fail
        return None  # Return None if all retries fail

    def format_text(self, text, app):
        key =  os.environ.get("GEMINI_API_KEY")
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

        parsed_data = self.process_request(URL, key, headers, data, app)
        if parsed_data is None:
            raise ValueError("Error fetching and parsing from Gemini")
        
        return parsed_data
    

