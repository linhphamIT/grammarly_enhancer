import google.generativeai as genai
import os
import json

# IMPORTANT: Store your API key securely, e.g., in an environment variable.
# Avoid hardcoding it directly in the source code in production environments.
API_KEY = "AIzaSyBhWBkTupWsGaEroX_NZGk21e0kJbvsiNE"

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('models/gemini-2.0-flash-lite')
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None

def call_gemini_api(text):
    """
    Calls the Google Gemini API to check grammar and provide enhancements.
    """
    if not model:
        return {
            "error": "Gemini model not initialized. Check API key configuration."
        }

    prompt = f"""Analyze the following sentence for grammar and provide enhancement suggestions.
Sentence: "{text}"

Please return the analysis in JSON format with the following structure: Ensure that the JSON response is valid and all property names are enclosed in double quotes.
{{
  "original_sentence": "The original sentence",
  "grammar_check": {{
    "is_correct": boolean,
    "explanation": "Detailed explanation of grammar correctness or errors."
  }},
  "enhancements": [
    {{
      "use_case": "Description of the context or nuance (e.g., More Formal, More Concise, Idiomatic Alternative)",
      "explanation": "Reason why this alternative might be chosen.",
      "alternatives": ["alternative sentence 1", "alternative sentence 2"]
    }}
  ]
}}

If the grammar is correct, provide at least two enhancement categories (e.g., More Concise, More Formal).
If the grammar is incorrect, the 'enhancements' array should contain suggestions for correction under a 'Grammar Correction' use_case.
"""

    response = None
    try:
        response = model.generate_content(prompt)
        # Attempt to parse the response as JSON
        # Gemini might return markdown ```json ... ```, so try to extract it
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        result = json.loads(response_text)
        return result
    except json.JSONDecodeError as e:
        print(f"Error decoding Gemini JSON response: {e}")
        print(f"Raw response: {response.text}")
        return {"error": "Failed to parse Gemini response as JSON.", "raw_response": response.text}
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        # Include response details if available
        error_details = f"Error: {e}"
        if hasattr(response, 'prompt_feedback'):
             error_details += f"\nPrompt Feedback: {response.prompt_feedback}"
        if hasattr(response, 'candidates') and response.candidates:
             error_details += f"\nFinish Reason: {response.candidates[0].finish_reason}"
             error_details += f"\nSafety Ratings: {response.candidates[0].safety_ratings}"

        return {"error": f"An error occurred during the Gemini API call. {error_details}"}

# Keep the placeholder functions for now, but they won't be used by main.py if tasks.py is updated
def google_gemini(text):
    """Placeholder, will be replaced by call_gemini_api usage."""
    return call_gemini_api(text) # Route to the actual API call

def check_grammar(text):
    """Uses the actual Gemini API call."""
    result = call_gemini_api(text)
    return result.get("grammar_check", {"error": result.get("error", "Unknown error")})

def enhance_grammar(text, analysis):
    """Uses the actual Gemini API call."""
    # Analysis is not strictly needed here as call_gemini_api does both
    result = call_gemini_api(text)
    return result.get("enhancements", [{"error": result.get("error", "Unknown error")}])
