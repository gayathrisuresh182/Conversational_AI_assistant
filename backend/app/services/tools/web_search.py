"""Web search tool using Tavily API."""
import httpx
from typing import Dict, Any
from app.config import settings


class WebSearchTool:
    """Tool for searching the web using Tavily API."""
    
    def __init__(self):
        self.api_key = settings.tavily_api_key
        self.base_url = "https://api.tavily.com"
    
    def search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Search the web for information.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary with search results
        """
        try:
            response = httpx.post(
                f"{self.base_url}/search",
                json={
                    "api_key": self.api_key,
                    "query": query,
                    "search_depth": "advanced",
                    "include_answer": True,
                    "include_raw_content": False,
                    "max_results": max_results,
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            
            # Format results
            results = {
                "answer": data.get("answer", ""),
                "results": []
            }
            
            for result in data.get("results", []):
                results["results"].append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "score": result.get("score", 0.0)
                })
            
            return results
            
        except Exception as e:
            return {
                "error": f"Web search failed: {str(e)}",
                "answer": "",
                "results": []
            }
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """Get tool definition for Claude function calling."""
        return {
            "name": "web_search",
            "description": "Search the internet for current information, news, facts, or any real-time data. Use this when the user asks about current events, recent information, or anything that requires up-to-date data.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look up on the internet"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }

