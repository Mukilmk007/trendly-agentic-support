from app.config import GEMINI_API_KEY, GEMINI_MODEL

print("Model:", GEMINI_MODEL)
print("Key prefix:", GEMINI_API_KEY[:12])

from app.services.gemini_service import GeminiService

gemini = GeminiService()

response = gemini.generate_text(
    system_prompt="You are a friendly assistant.",
    user_prompt="Say hello in one sentence."
)

print(response)