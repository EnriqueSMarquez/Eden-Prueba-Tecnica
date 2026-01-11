from google import genai
from google.genai import types
from PIL import Image

class GeminiClient:
    def __init__(self, api_key: str, gemini_model: str = "gemini-3-pro-preview"):
        self.client = genai.Client(api_key=api_key)
        self.model = gemini_model
    def predict(self, system_instruction: str, prompt: str, temperature: float, image: Image.Image = None) -> str:
        
        if image is not None:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt, image],
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temperature
                )
            )
        else:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temperature
                )
            )
        return response.text
