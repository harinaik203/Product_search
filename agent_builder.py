import os
from dataclasses import dataclass
from dotenv import load_dotenv

from exception import CustomException

from agno.agent import Agent, RunResponse
from agno.models.google import Gemini
from agno.tools.serpapi import SerpApiTools
from agno.tools.googlesearch import GoogleSearchTools

# Load environment variables
load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")


@dataclass
class ProductAgent:
    """
    Builds a product search agent that fetches
    real-time product price information from the web.
    """

    def build_agent(self) -> Agent:
        try:
            # Initialize Gemini LLM
            llm_model = Gemini(
                id="gemini-2.5-flash-lite",
                api_key=GOOGLE_API_KEY,
                temperature=0.1,
                max_output_tokens=2048
            )

            # Build the web search agent
            web_search_agent = Agent(
                name="Product Search Agent",
                role="Search the web for verified product pricing information in India.",
                model=llm_model,
                tools=[
                    SerpApiTools(api_key=SERP_API_KEY),
                    GoogleSearchTools()
                ],
                description=[
                    "You are a product search expert that must rely on web search tools for pricing."
                ],
                instructions="""
You are NOT allowed to answer from memory.

Step 1: Search the web using SerpApiTools for product prices in India
Step 2: Verify results using GoogleSearchTools
Step 3: Extract prices in Indian Rupees (₹)
Step 4: If multiple prices are found, show a range
Step 5: Provide source links

Rules:
- Use web search results ONLY
- Do NOT say "price not found" if any result exists
- Prefer Indian sellers and official sources
- Do NOT hallucinate prices
""",
                goal="Retrieve real-time product pricing information from Indian online sources.",
                tool_call_limit=10,
                show_tool_calls=False,
                markdown=True
            )

            return web_search_agent

        except Exception as e:
            raise CustomException(e)

    def perform_task(self, task: str) -> RunResponse:
        try:
            agent = self.build_agent()
            response: RunResponse = agent.run(task)
            return response
        except Exception as e:
            raise CustomException(e)
