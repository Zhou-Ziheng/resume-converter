import json
import logging
import os
import time
import requests


URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key="


class GoogleGenimiWrapper:
    gemini_client = None

    @classmethod
    def get_one(cls):
        if cls.gemini_client is None:
            cls.gemini_client = GoogleGenimiWrapper()
            cls.gemini_client.prompt = open("src/Convert/prompt.txt", "r").read()
            cls.gemini_client.structure = open("src/Convert/structure.json", "r").read()
        return cls.gemini_client

    def process_request(self, URL, key, headers, data):
        retries = 3  # Number of retries
        for attempt in range(retries):
            try:
                # Send POST request
                response = requests.post(URL + key, headers=headers, json=data)
                response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
                data = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                parsed_data = json.loads(data, strict=False)
                return parsed_data  # Return parsed data if successful
            except requests.RequestException as e:
                logging.error(f"Error processing request: {e}")
                logging.error(f"Response: {response.json()['error']}")
                if attempt < retries - 1:
                    logging.warning("Retrying...")
                    time.sleep(5)  # Wait before retrying
            except (KeyError, IndexError) as e:
                logging.error(f"Error processing request: {e}")
                if attempt < retries - 1:
                    logging.warning("Retrying...")
                    time.sleep(5)  # Wait before retrying
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON: {e} \n {data}")
                if attempt < retries - 1:
                    logging.warning("Retrying...")
                    time.sleep(10)

        logging.error("All retries failed.")
        raise Exception("All retries failed.")  # Raise an exception if all retries fail

    def format_text(self, text):
        key = os.environ.get("GEMINI_API_KEY")
        data = {
            "contents": [{"parts": [{"text": self.prompt + self.structure + text}]}],
            "generationConfig": {"response_mime_type": "application/json"},
        }

        headers = {"Content-Type": "application/json"}

        parsed_data = self.process_request(URL, key, headers, data)

        return parsed_data
