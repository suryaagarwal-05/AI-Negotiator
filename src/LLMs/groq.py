from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import os

class GroqLLM:
    def get_llm_model(model_name="llama-3.3-70b-versatile", api_key=None):
        # Fetch the API key from environment if not specified
        if api_key is None:
            api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is not set in the environment or passed as an argument.")

        return ChatGroq(api_key=api_key, model=model_name)
