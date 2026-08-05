from app.services.gemini_service import GeminiService

gemini = GeminiService()

observations = [
    {
        "success": True,
        "tool": "lookup_order",
        "data": {
            "order_id": "TR-4521",
            "status": "in_transit",
            "carrier": "BlueDart",
            "expected_delivery": "2026-07-31"
        },
        "error": None
    }
]

response = gemini.generate_response(
    "Where is my order TR-4521?",
    observations
)

print(response)