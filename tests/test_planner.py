from app.services.gemini_service import GeminiService

gemini = GeminiService()

print("Calling planner...")

plan = gemini.plan("Where is my order TR-4521?")

print(plan)