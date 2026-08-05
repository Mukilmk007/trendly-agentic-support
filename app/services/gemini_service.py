import json
import time

from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.prompts.planner_prompt import PLANNER_SYSTEM_PROMPT
from app.prompts.response_prompt import RESPONSE_SYSTEM_PROMPT


class GeminiService:

    MAX_RETRIES = 3
    RETRY_DELAY = 2

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = GEMINI_MODEL

    def _generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        response_mime_type: str | None = None,
    ):

        last_exception = None

        for attempt in range(self.MAX_RETRIES):

            try:

                config = types.GenerateContentConfig(
                    temperature=temperature
                )

                if response_mime_type:
                    config.response_mime_type = response_mime_type

                return self.client.models.generate_content(
                    model=self.model,
                    contents=[
                        system_prompt,
                        user_prompt
                    ],
                    config=config
                )

            except Exception as e:

                last_exception = e

                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(self.RETRY_DELAY)

        raise RuntimeError(
            f"Gemini API Error after {self.MAX_RETRIES} attempts: {last_exception}"
        )

    def generate_text(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
    ) -> str:

        response = self._generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature
        )

        return response.text.strip()

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
    ) -> dict:

        response = self._generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            response_mime_type="application/json"
        )

        try:
            return json.loads(response.text)

        except json.JSONDecodeError:
            raise ValueError("Gemini returned invalid JSON.")

    def plan(
            self,
            user_message: str,
            state
        ) -> dict:

            planner_context = state.get_planner_context()

            prompt = f"""
        Conversation History:
        {json.dumps(planner_context["history"], indent=2)}

        Current Order:
        {json.dumps(planner_context["current_order"], indent=2)}

        Current Policy:
        {json.dumps(planner_context["current_policy"], indent=2)}

        Latest User Message:
        {user_message}
        """

            return self.generate_json(
                system_prompt=PLANNER_SYSTEM_PROMPT,
                user_prompt=prompt,
                temperature=0.0
            )


    def generate_response(
        self,
        user_message: str,
        observations,
        state
    ) -> str:

        prompt = f"""
    User Question:
    {user_message}

    Tool Results:
    {json.dumps(observations, indent=2)}

    Write a concise, friendly customer support response.

    Use ONLY the tool results above.
    Do not invent any information.
    """

        return self.generate_text(
            system_prompt=RESPONSE_SYSTEM_PROMPT,
            user_prompt=prompt,
            temperature=0.2
        )