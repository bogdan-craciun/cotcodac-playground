import requests

# current weather
# https://api.open-meteo.com/v1/forecast?latitude=46.9481&longitude=7.4474&current=temperature_2m,relative_humidity_2m,rain,weather_code
response = requests.get(
    "https://api.open-meteo.com/v1/forecast?latitude=45.7983&longitude=24.1256&current_weather=true"
)
weather_data = response.json()

current_weather = weather_data["current_weather"]
temperature = current_weather["temperature"]
humidity = current_weather["relative_humidity"]
conditions = current_weather["weather_code"]

print(f"Current temperature: {temperature}°C")
print(f"Current humidity: {humidity}%")
print(f"Weather conditions: {conditions}")
