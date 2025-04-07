from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os # To potentially get port from environment for deployment

# Import the existing function that calls the API
# Assuming it's correctly located relative to this file
try:
    from grammarly_enhancer.tools.grammar_tool import call_gemini_api
except ImportError:
    # Handle case where the structure might be slightly different when run directly
    from .tools.grammar_tool import call_gemini_api


# --- Pydantic Model for Request Body ---
class GrammarRequest(BaseModel):
    text: str


# --- FastAPI App Initialization ---
app = FastAPI(
    title="Grammarly Enhancer API",
    description="API to analyze and enhance text using CrewAI/Gemini.",
    version="0.1.0"
)


# --- API Endpoint ---
@app.post("/enhance", summary="Enhance Grammar", description="Receives text and returns grammar analysis and enhancements.")
async def enhance_grammar(request: GrammarRequest):
    """
    Analyzes and enhances grammar for the input text using the Google Gemini API.
    Accepts a JSON body like: {"text": "your input sentence here"}
    Returns a JSON object with analysis and enhancements.
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    try:
        # Call the existing API function with text from the request
        gemini_response = call_gemini_api(request.text)

        # Process the response
        if "error" in gemini_response:
            # Return a server error if the underlying API call failed
            raise HTTPException(status_code=500, detail=f"Error calling backend API: {gemini_response['error']}")

        original_sentence = gemini_response.get("original_sentence", request.text)
        analysis = gemini_response.get("grammar_check", {})
        enhanced_sentences = gemini_response.get("enhancements", [])

        # Build a structured response
        response_data = {
            "original_sentence": original_sentence,
            "grammar_check": analysis,
            "enhancements": enhanced_sentences
        }

        return response_data # FastAPI automatically converts dict to JSON response

    except Exception as e:
        # Catch any other unexpected errors during processing
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")


# --- Root Endpoint (Optional) ---
@app.get("/", summary="Root", description="Basic endpoint to check if the API is running.")
async def read_root():
    return {"message": "Grammarly Enhancer API is running."}


# --- Uvicorn Runner for Local Execution ---
if __name__ == "__main__":
    # Get port from environment variable or default to 8000
    # Useful for deployment platforms like Render that set a PORT env var
    port = int(os.environ.get("PORT", 8000))
    # Run the FastAPI app locally
    # Set reload=False for production environments
    # Host '0.0.0.0' makes it accessible on the network
    uvicorn.run("grammarly_enhancer.main:app", host="0.0.0.0", port=port, reload=False)
