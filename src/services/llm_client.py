import os
from google import genai

class LLMClient:

    def __init__(self):
        api_key = os.getenv("LLM_API_KEY")

        self.model = os.getenv("LLM_MODEL_NAME", "gpt-4")
        self.client = genai.Client(api_key=api_key)

    def complete(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text.strip()