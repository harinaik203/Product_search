import os
from dataclasses import dataclass
from dotenv import load_dotenv

from exception import CustomException

from agno.agent import Agent, RunResponse
from agno.models.openrouter import OpenRouter

# Load environment variables
load_dotenv()

# API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


@dataclass
class ProductAgent:
    """
    LLM-only Product Search Agent.
    Generates realistic price insights for products in the Indian market.
    """

    def build_agent(self) -> Agent:
        try:
            # Initialize OpenRouter LLM (no tool calling)
            llm_model = OpenRouter(
                id="mistralai/mistral-7b-instruct",
                api_key=OPENROUTER_API_KEY,
                temperature=0.2,
                max_tokens=2048
            )

            agent = Agent(
                name="Product Search Agent",
                role="Generate product price insights for the Indian market.",
                model=llm_model,
                instructions="""
You are a product price analysis assistant for India.

TASK:
- Provide a realistic price overview for the given product in India.

GUIDELINES:
- Mention common Indian platforms such as Amazon, Flipkart, local retailers
- Provide approximate price ranges in INR (₹)
- Clearly state that prices may vary by seller, location, and time
- Do NOT claim real-time verification
- Do NOT generate fake product links
- Be clear, structured, and concise

OUTPUT FORMAT:
## Product Overview
## Estimated Price Range (India)
## Popular Platforms
## Notes / Disclaimer
""",
                markdown=True
            )

            return agent

        except Exception as e:
            raise CustomException(e)

    def perform_task(self, task: str) -> RunResponse:
        try:
            agent = self.build_agent()
            response: RunResponse = agent.run(task)
            return response
        except Exception as e:
            raise CustomException(e)
