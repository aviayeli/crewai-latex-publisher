import requests
from crewai.tools import BaseTool
from pydantic import BaseModel

from src.config import settings

_URL = "https://api.perplexity.ai/chat/completions"


class PerplexitySearchInput(BaseModel):
    query: str
    max_results: int = 5


class PerplexitySearchTool(BaseTool):
    name: str = "perplexity_search"
    description: str = (
        "Queries Perplexity AI sonar-pro for academic research sources."
    )
    args_schema: type[BaseModel] = PerplexitySearchInput

    def _run(self, query: str, max_results: int = 5) -> str:
        if not query.strip():
            raise ValueError("query must not be empty")
        payload = {
            "model": "sonar-pro",
            "messages": [{"role": "user", "content": query}],
        }
        headers = {
            "Authorization": f"Bearer {settings.PERPLEXITY_API_KEY}",
            "Content-Type": "application/json",
        }
        response = requests.post(_URL, headers=headers, json=payload)
        if response.status_code == 429:
            response.raise_for_status()
        elif response.status_code >= 400:
            raise ValueError(
                f"HTTP {response.status_code} from Perplexity API"
            )
        return response.json()["choices"][0]["message"]["content"]


perplexity_search_tool = PerplexitySearchTool()
