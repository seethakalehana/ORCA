
import time
from groq import Groq
from backend.config import GROQ_API_KEY
from agents.gemini_agent import explain_marine_conditions

groq_client = Groq(api_key=GROQ_API_KEY)


def get_marine_explanation(ocean_conditions, risk_result):

    for attempt in range(3):
        try:
            response = explain_marine_conditions(
                ocean_conditions, risk_result
            )

            if response and not response.startswith(
                "Sorry, ORCA could not generate"
            ):
                return response

        except Exception as error:
            print("Gemini error:", error)

        if attempt < 2:
            time.sleep(2)

    print("Switching to Groq backup...")

    try:
        prompt = f"""
        Explain these marine conditions:
        {ocean_conditions}

        Risk assessment:
        {risk_result}
        Do not invent measurements.
        """

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as error:
        print("Groq error:", error)
        return "Both AI models are currently unavailable."
