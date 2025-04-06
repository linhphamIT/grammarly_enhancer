

from grammarly_enhancer.tools.grammar_tool import call_gemini_api


def run():
    """
    Main function (renamed to 'run' for crew compatibility) to analyze and enhance grammar using the Google Gemini API.
    """
    # Call the API once to get the full response
    text = input("Enter input: ")
    gemini_response = call_gemini_api(text)

    if "error" in gemini_response:
        return f"Error calling Gemini API: {gemini_response['error']}"

    original_sentence = gemini_response.get("original_sentence", text) # Use original from response if available
    analysis = gemini_response.get("grammar_check", {})
    enhanced_sentences = gemini_response.get("enhancements", [])

    result = f"Original Sentence: \"{original_sentence}\"\n\n"

    # Display Grammar Check
    result += "Grammar Check:\n\n"
    if "explanation" in analysis:
        result += f"{analysis['explanation']}\n\n"
    elif "error" in analysis:
         result += f"Error during grammar check: {analysis['error']}\n\n"
    else:
        result += "Grammar check information not available.\n\n"

    # Display Enhancements
    result += "Enhancements & Alternatives (Depending on Context/Desired Nuance):\n\n"
    if enhanced_sentences:
        for enhancement in enhanced_sentences:
            if "error" in enhancement:
                result += f"Error retrieving enhancement: {enhancement['error']}\n\n"
                continue
            result += f"Use Case: {enhancement.get('use_case', 'N/A')}\n"
            result += f"Explanation: {enhancement.get('explanation', 'N/A')}\n"
            alternatives = enhancement.get('alternatives', [])
            if alternatives:
                result += "Alternatives:\n"
                for alt in alternatives:
                    result += f"- {alt}\n"
            result += "\n" # Add space between enhancement sections
    else:
        result += "No enhancement suggestions provided.\n\n"


    print(result)
    return result
