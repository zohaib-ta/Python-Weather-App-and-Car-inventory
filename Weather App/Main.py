import datetime as dt
import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = "7039b1b0634ecccf5f7bb2b658d7cdbf"

def welcome_message():
    print("Welcome to Zohaib's Weather App!")
    print("Get live weather information for your desired city.\n")

def get_city_input(available_cities):
    while True:
        city = input("Enter the city name for the weather forecast: ").strip().capitalize()
        if city in available_cities:
            return city
        else:
            print(f"Sorry, '{city}' is not in our list of cities. Please try again.\n")

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit

def fetch_weather_data(city):
    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp_kelvin = data['main']['temp']
        temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
        feels_like_kelvin = data['main']['feels_like']
        feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
        windspeed = data['wind']['speed']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        
        return {
            "temperature_c": temp_celsius,
            "temperature_f": temp_fahrenheit,
            "feels_like_c": feels_like_celsius,
            "feels_like_f": feels_like_fahrenheit,
            "wind_speed": windspeed,
            "humidity": humidity,
            "condition": description.capitalize()
        }
    else:
        print(f"Error: Unable to gather weather data for {city}. Please try again.")
        return None

def display_weather_data(city, data):
    print(f"\nWeather in {city}:")
    print(f"Temperature: {data['temperature_c']:.2f} °C | {data['temperature_f']:.2f} °F")
    print(f"Feels Like: {data['feels_like_c']:.2f} °C | {data['feels_like_f']:.2f} °F")
    print(f"Weather Condition: {data['condition']}")
    print(f"Wind Speed: {data['wind_speed']} m/s")
    print(f"Humidity: {data['humidity']}%")

def thank_you_message():
    print("\nThank you for using Zohaib's Weather Forecast App! Have a great day!")

def main():
    welcome_message()
    
    # List of available cities 
    available_cities = ["London", "Paris", "New York", "Tokyo"]
    
    city = get_city_input(available_cities)
    weather_data = fetch_weather_data(city)
    
    if weather_data:
        display_weather_data(city, weather_data)
    
    thank_you_message()

if __name__ == "__main__":
    main()



