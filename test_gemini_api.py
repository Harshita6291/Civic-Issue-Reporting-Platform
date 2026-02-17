import requests
import json

gemini_api_key = "AIzaSyD7lGUGs-5S0BuFUVHXZFeO2uR9OdaICJQ"
gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + gemini_api_key

# Example complaint (simulate reading from issues.json)
complaint = {
    "ticket_id": "test-123",
    "description": "There is a large pile of garbage in my area that has not been cleaned for weeks. It smells and attracts stray animals.",
    "category": "Garbage/Waste Management",
    "urgency": "High"
}

system_prompt = "You are a civic issue assistant. Only provide suggestions based on the current complaint details."
user_content = f"Complaint details: {json.dumps(complaint)}"
payload = {
    "contents": [
        {"role": "system", "parts": [{"text": system_prompt}]},
        {"role": "user", "parts": [{"text": user_content}]}
    ]
}

try:
    response = requests.post(gemini_url, json=payload)
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    if response.status_code == 200:
        data = response.json()
        if "candidates" in data and len(data["candidates"]) > 0:
            suggestion_text = data["candidates"][0]["content"]["parts"][0]["text"]
            print("AI Suggestions:")
            print(suggestion_text)
        else:
            print("No AI suggestions returned.")
    else:
        print("Error from Gemini API.")
except Exception as e:
    print("Exception:", e)
