from app.services.gemini_service import GeminiService

gemini = GeminiService()

response = gemini.generate_json(
    system_prompt="""
Return JSON only.

{
    "city":"",
    "country":""
}
""",
    user_prompt="Paris is in France"
)

print(response)