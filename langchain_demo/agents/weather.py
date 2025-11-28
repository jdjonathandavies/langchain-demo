from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph

load_dotenv()


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


class WeatherAgent:
    def __init__(self) -> None:
        self.agent: CompiledStateGraph = create_agent(
            model="google_genai:gemini-2.5-flash-lite",
            tools=[get_weather],
            system_prompt="You are a helpful assistant",
        )

    def get_weather(self, location: str) -> str:
        response = self.agent.invoke(
            {
                "messages": [
                    {"role": "user", "content": f"what is the weather in {location}"}
                ]
            }
        )
        return response["messages"][-1]
