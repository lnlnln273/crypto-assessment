import json
from google import genai
from google.genai import types

class GeminiClient:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.model_name = model_name

    def analyze_market(self, indicators_json: dict = None, custom_prompt: str = None) -> str:
        client = genai.Client()
        input_data = {
            "task": "crypto_market_analysis",
            "prompt": custom_prompt,
            "indicators": indicators_json
        }

        response = client.models.generate_content(
            model=self.model_name,
            contents=json.dumps(input_data),
            config=types.GenerateContentConfig(temperature=0.5)
        )

        return response.text