import re
import spacy
import requests
import json

# Load the spaCy model for English
nlp = spacy.load("en_core_web_sm")

# Mapping for word numbers to digits
word_to_num = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
    'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12
}

# List of relevant activities we want to extract (verbs related to outdoor activities)
relevant_activities = ["swim", "run", "climb", "hike", "cycle", "attend"]

# Function to extract city, days, and activities from the prompt
def extract_info(prompt):
    # Updated regex to catch phrases like "going to", "want to go to", etc.
    city_pattern = r"(?:going to|want to go to|heading to|visit|go to) (\w+)"
    days_pattern = r"for (?:at least )?(\d+) days|(\w+) days|(\w+) week"

    # Extract city name
    city_match = re.search(city_pattern, prompt)
    city = city_match.group(1) if city_match else None

    # Extract number of days
    days_match = re.search(days_pattern, prompt)
    if days_match:
        if days_match.group(1):  # Numeric days (e.g., "3 days")
            days = days_match.group(1)
        elif days_match.group(2):  # Word-based days (e.g., "seven days")
            days = word_to_num.get(days_match.group(2).lower())
        elif days_match.group(3):  # Week-based (e.g., "one week")
            days = word_to_num.get(days_match.group(3).lower()) * 7 if days_match.group(3).lower() in word_to_num else None
    else:
        days = None

    # Use spaCy to process the prompt and extract verbs (activities)
    doc = nlp(prompt)
    activities = [token.lemma_ for token in doc if token.pos_ == "VERB" and token.lemma_ in relevant_activities]

    # Remove the city from activities if mentioned
    if city:
        activities = [activity for activity in activities if activity.lower() != city.lower()]

    return {"city": city, "days": days, "activities": activities}

# Function to fetch weather information using OpenWeatherMap API
def get_weather_info(city):
    api_key = '10590029bc203e7dc2c0dbecf4c50d88'  # Replace with your OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    # Make an API request to OpenWeatherMap
    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.json()
        # Extract temperature, humidity, and rainfall (if available)
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        rainfall = data.get('rain', {}).get('1h', 0)  # Rainfall in the last 1 hour (if available)

        return {
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall
        }
    else:
        # Print the full response to debug
        print(f"Error: {response.status_code} - {response.reason}")
        print("Response Content:", response.json())  # Full response for debugging
        return {"error": "City not found or API request failed."}

# Function to recommend clothes based on weather, terrain, and activities
def recommend_clothes_from_json(temperature, humidity, rainfall, city, activities, data):
    recommendations = []

    # Check if the city exists in the terrain-based recommendations
    city_found = False
    for terrain_category, terrain_info in data["terrain_based_recommendations"].items():
        if city in terrain_info["cities"]:
            # Add recommendations based on the city's terrain
            recommendations.extend(terrain_info["recommendations"])
            city_found = True
            break

    # If no specific city recommendation is found, proceed based on weather
    if not city_found:
        print(f"No specific city recommendations found for {city}. Proceeding with weather-based recommendations.")

    # Temperature-based recommendations
    if temperature < 10:
        recommendations.extend(data["temperature"]["very_cold"]["recommendations"])
    elif 10 <= temperature < 20:
        recommendations.extend(data["temperature"]["cold"]["recommendations"])
    elif 20 <= temperature < 30:
        recommendations.extend(data["temperature"]["mild"]["recommendations"])
    else:
        recommendations.extend(data["temperature"]["hot"]["recommendations"])

    # Humidity-based recommendations
    if humidity > 70:
        recommendations.extend(data["humidity"]["high"]["recommendations"])
    elif humidity < 30:
        recommendations.extend(data["humidity"]["low"]["recommendations"])

    # Rainfall-based recommendations
    if rainfall > 0:
        recommendations.extend(data["rainfall"]["rain_detected"]["recommendations"])
    else:
        recommendations.extend(data["rainfall"]["no_rain"]["recommendations"])

    # Activity-based recommendations
    for activity in activities:
        if activity in data["activities"]:
            recommendations.extend(data["activities"][activity]["recommendations"])

    return recommendations

# Load the recommendations from the JSON file
with open('weather_clothing_recommendations.json', 'r') as json_file:
    recommendations_data = json.load(json_file)

# Let the user enter the prompt
prompt = input("Enter your prompt: ")

# Extract information from the prompt
info = extract_info(prompt)

# Display the extracted information
print("\nExtracted Information:")
print("City:", info["city"])
print("Days:", info["days"])
print("Activities:", ", ".join(info["activities"]) if info["activities"] else "None")

# Fetch weather information for the extracted city
if info["city"]:
    weather_info = get_weather_info(info["city"])

    if 'error' not in weather_info:
        print(f"\nWeather Information for {info['city'].capitalize()}:")
        print(f"Temperature: {weather_info['temperature']}°C")
        print(f"Humidity: {weather_info['humidity']}%")
        print(f"Rainfall: {weather_info['rainfall']} mm")

        # Get clothing recommendations based on the weather, terrain, and activities
        clothing_recommendations = recommend_clothes_from_json(
            weather_info['temperature'], weather_info['humidity'], weather_info['rainfall'], info['city'], info['activities'], recommendations_data
        )

        # Display the clothing recommendations
        print("\nBased on the weather conditions, terrain, and activities, you should consider the following clothes:")
        for recommendation in clothing_recommendations:
            print("-", recommendation)
    else:
        print(weather_info['error'])
else:
    print("City not found in the prompt.")
