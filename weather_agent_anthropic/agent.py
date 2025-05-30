from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts


MODEL_CLAUDE_SONNET = "anthropic/claude-opus-4-20250514"

# @title Define the get_weather Tool
def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: get_weather called for city: {city} ---") # Log tool execution
    city_normalized = city.lower().replace(" ", "") # Basic normalization

    # Mock weather data
    mock_weather_db = {
        "newyork": {"status": "success", "report": "The weather in New York is sunny with a temperature of 25°C."},
        "london": {"status": "success", "report": "It's cloudy in London with a temperature of 15°C."},
        "tokyo": {"status": "success", "report": "Tokyo is experiencing light rain and a temperature of 18°C."},
    }

    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {"status": "error", "error_message": f"Sorry, I don't have weather information for '{city}'."}
    

root_agent = Agent(
    name="weather_agent_claude",
    # Key change: Wrap the LiteLLM model identifier
    model=LiteLlm(model=MODEL_CLAUDE_SONNET),
    description="Provides weather information (using Claude).",
    instruction="You are a helpful weather assistant powered by Anthropic's Claude model. "
                "Use the 'get_weather' tool for city weather requests. "
                "Clearly present successful reports or polite error messages based on the tool's output status.",
    tools=[get_weather], # Re-use the same tool
    )