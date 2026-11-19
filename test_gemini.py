
from agents.gemini_agent import ask_gemini

question = "Hello ORCA! Introduce yourself briefly."

print("Testing ORCA Gemini connection...")

answer = ask_gemini(question)

print("\nGemini Response:")
print(answer)
