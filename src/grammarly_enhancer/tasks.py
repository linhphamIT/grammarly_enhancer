from .tools.grammar_tool import call_gemini_api

def analyze_text_task(text):
    """
    Analyzes the text input. (Currently not used with Gemini approach)
    """
    return ""

def check_grammar_task(text):
    """
    Checks the grammar and vocabulary using the Gemini API.
    """
    gemini_response = call_gemini_api(text)
    if "error" in gemini_response:
        return {"error": gemini_response["error"]}
    return gemini_response.get("grammar_check", {"error": "Grammar check data missing from API response."})

def identify_scenarios_task(text):
    """
    Identifies the scenarios. (Currently not used with Gemini approach)
    """
    return []

def enhance_grammar_task(text):
    """
    Enhances the grammar of the sentences using the Gemini API.
    Note: The 'analysis' parameter is removed as call_gemini_api handles both check and enhancement.
    """
    gemini_response = call_gemini_api(text)
    if "error" in gemini_response:
        return [{"error": gemini_response["error"]}]
    return gemini_response.get("enhancements", [{"error": "Enhancements data missing from API response."}])
