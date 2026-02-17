import google.generativeai as genai
import json

genai_api_key = "AIzaSyD7lGUGs-5S0BuFUVHXZFeO2uR9OdaICJQ"

# Example complaint (simulate reading from issues.json)
complaint = {
    "ticket_id": "test-123",
    "description": "There is a large pile of garbage in my area that has not been cleaned for weeks. It smells and attracts stray animals.",
    "category": "Garbage/Waste Management",
    "urgency": "High"
}

genai.configure(api_key=genai_api_key)

system_prompt = "You are a civic issue assistant. Only provide suggestions based on the current complaint details."
user_content = f"Complaint details: {json.dumps(complaint)}"

try:
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content([
        system_prompt,
        user_content
    ])
    print("Response:", response.text)
except Exception as e:
    print("Exception:", e)
