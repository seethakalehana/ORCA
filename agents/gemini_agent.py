
from google import genai
from backend.config import GEMINI_API_KEY, GEMINI_MODEL

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


def ask_gemini(question: str) -> str:
    """
    Send a question to Gemini and return its response.
    """

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=question
        )

        return response.text or "Gemini returned an empty response."

    except Exception as error:
        print("Gemini error:", error)
        return "Sorry, ORCA could not generate a response right now."

def explain_marine_conditions(ocean_conditions, risk_result):

    prompt = f"""
    You are ORCA, a Marine Intelligence Assistant.

    Analyze the following ocean conditions:

    Ocean Conditions:
    {ocean_conditions}

    Marine Risk Assessment:
    {risk_result}

    Explain:
    1. Current ocean conditions.
    2. Potential marine risk indicators.
    3. Why these indicators matter.
    4. Precautions users should consider.

    Use simple, clear language.
    Do not invent ocean measurements or claim that this
    preliminary assessment is an official marine warning.
    """

    return ask_gemini(prompt)
def answer_marine_question(question, ocean_conditions, risk_result):
    prompt = f"""
    You are ORCA, a Marine Intelligence Assistant.

    User question: {question}

    Actual ocean conditions:
    {ocean_conditions}

    Preliminary risk assessment:
    {risk_result}

    Answer the user's question using the supplied ocean data
    wherever relevant. Do not invent measurements.
    Explain clearly and simply.
    """

    return ask_gemini(prompt)
def explain_inland_conditions(weather_conditions, risk_result):
    prompt = f"""
    You are ORCA, an Inland Weather Intelligence Assistant.

    Current Weather Conditions:
    {weather_conditions}

    Preliminary Weather Risk Assessment:
    {risk_result}

    Explain:
    1. Current weather conditions.
    2. Potential weather risk indicators.
    3. Why these indicators matter.
    4. Practical precautions users can consider.

    Use simple language.
    Do not invent measurements.
    Do not present this as an official weather warning.
    """

    return ask_gemini(prompt)