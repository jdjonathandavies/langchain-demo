from flask import Flask
from langchain_demo.agents.weather import WeatherAgent

app = Flask(__name__)

AGENT = WeatherAgent()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/weather/<location>")
def get_weather(location: str):
    return AGENT.get_weather(location)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
