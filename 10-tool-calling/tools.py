"""
Module 10 — Tool Calling Schema & Implementation
"""

from google.genai import types


def get_weather(city: str) -> dict:
    """Mock weather tool returning current condition and temperature."""
    mock_data = {
        "Mumbai": {"temperature_c": 32, "condition": "Humid and partly cloudy"},
        "Delhi": {"temperature_c": 28, "condition": "Sunny with haze"},
        "Pune": {"temperature_c": 25, "condition": "Pleasant and clear"},
        "Bangalore": {"temperature_c": 22, "condition": "Mild and cloudy"},
    }
    return mock_data.get(city, {"temperature_c": None, "condition": f"No data for {city}"})


weather_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_weather",
            description="Returns current weather information for a specified city.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "city": types.Schema(
                        type=types.Type.STRING,
                        description="The name of the city, e.g. 'Mumbai', 'Delhi'.",
                    )
                },
                required=["city"],
            ),
        )
    ]
)

TOOL_REGISTRY = {
    "get_weather": get_weather,
}
