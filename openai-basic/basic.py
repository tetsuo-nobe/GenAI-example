import os

# OpenAI API Key のインポート
os.environ["OPENAI_API_KEY"] = ""

import openai

# Hello
print("--- Hello --------------------------------------------")
response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! I'm John."}
    ]
)
print(response)

#
print("--- history --------------------------------------------")
response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! I'm John."},
        {"role": "assistant","content": "Hello John! How can I assist you today?"},
        {"role": "user", "content": "Do you know my name?"}
    ]
)
print(response)

#
print("--- Stream --------------------------------------------")

response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! I'm John."}
    ],
    stream=True
)
for chunk in response:
  choice = chunk["choices"][0]
  if choice["finish_reason"] is None:
    print(choice["delta"]["content"])

#
print("--- Function --------------------------------------------")

import json
def get_current_weather(location, unit="celsius"):
  weather_info = {
      "location": location,
      "temperature": "25",
      "unit": "celsius",
      "forecast": ["sunny","windy"],
  }
  return json.dumps(weather_info)

functions = [
      {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. Tokyo",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius","fahrenheit"]
                },
            },
            "required": ["location"],
        },
  }
]

messages = [
    {"role":"user", "content":"What's the weather like in Tokyo?"}
]

response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages=messages,
    functions= functions
)
print(response)

