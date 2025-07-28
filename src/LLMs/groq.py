# src/LLMs/groq.py
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

class GroqLLM:
    _mcp_client = None
    _tools = None
    
    @classmethod
    async def _initialize_mcp_client(cls):
        """Initialize MCP client once for the class"""
        if cls._mcp_client is None:
            cls._mcp_client = MultiServerMCPClient({
                "tavily": {
                    "url": "https://server.smithery.ai/@tavily-ai/tavily-mcp/mcp?api_key=2d235323-4264-4c9d-9c8a-f317dbad8514&profile=invisible-platypus-MViQZ2&max_results=1",
                    "transport": "streamable_http",
                }
            })
            cls._tools = await cls._mcp_client.get_tools()
    
    @staticmethod
    def get_llm_model(model_name="llama-3.3-70b-versatile", api_key=None):
        """Get basic LLM model without tools"""
        if api_key is None:
            api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is not set in the environment or passed as an argument.")

        return ChatGroq(api_key=api_key, model=model_name)
    
    @classmethod
    async def get_llm_with_tools(cls, model_name="deepseek-r1-distill-llama-70b", api_key=None):
        """Get LLM model with tools bound (agent)"""
        # Initialize MCP client and get tools
        await cls._initialize_mcp_client()
        
        # Get base model
        base_model = cls.get_llm_model(model_name, api_key)
        
        # Create agent with tools bound
        agent = create_react_agent(base_model, cls._tools)
        
        return agent
    
    @classmethod
    async def get_search_tools(cls):
        """Get just the tools for manual use if needed"""
        await cls._initialize_mcp_client()
        return cls._tools