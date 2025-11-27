from logging import getLogger
from flask import Flask
from langchain_demo.agents.weather import WeatherAgent

LOGGER = getLogger(__name__)
AGENT = WeatherAgent()

app = Flask(__name__)


@app.route("/")
def hello_world() -> str:
    return "<p>Hello, World!</p>"


@app.route("/weather/<location>")
def get_weather(location: str) -> str:
    LOGGER.info(f"getting weather for {location}")
    weather_message = AGENT.get_weather(location)
    LOGGER.info(f"got weather message '{weather_message}'")
    return weather_message


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
