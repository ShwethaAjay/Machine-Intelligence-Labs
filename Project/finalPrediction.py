import pandas as pd
import joblib
import requests
from datetime import datetime


def compare_cost(current_kwh, predicted_solar_kwh, current_cost_per_kwh=0.1683):
    current_cost = current_kwh * current_cost_per_kwh
    solar_cost = 47.50  # Average monthly cost of maintenance

    savings = current_cost - solar_cost
    roi_years = 10000 / savings if savings > 0 else float('inf')  # Assumes $10,000 investment for solar

    print(f"\n--- Cost Comparison Analysis ---\n")
    print(f"Current Monthly Electricity Usage (kWh): {current_kwh:.2f}")
    print(f"Predicted Solar Power Generation (kWh): {predicted_solar_kwh:.2f}")
    print(f"Current Monthly Cost (USD): ${current_cost:.2f}")
    print(f"Potential Savings with Solar (USD/month): ${savings:.2f}")
    if roi_years != float('inf'):
        print(f"Estimated Return on Investment: {roi_years:.2f} years")
    else:
        print("Solar adoption may not yield savings with the current inputs.")


# ----------------------------------------------
# Function to Get User Input for Electricity Generation
# ----------------------------------------------
def get_user_input():
    """
    Collect user inputs for predicting electricity generation.
    Returns a Pandas DataFrame with the inputs.
    """
    input_features = ['num_rooms', 'num_people', 'housearea', 'is_ac', 'is_tv', 'is_flat',
                      'ave_monthly_income', 'num_children', 'is_urban']

    print("\nEnter the following details for electricity generation prediction:\n")
    user_data = {}

    for feature in input_features:
        if feature in ['is_ac', 'is_tv', 'is_flat', 'is_urban']:  # Handle boolean inputs
            value = input(f"Is {feature[3:]} available? (yes/no): ").strip().lower()
            while value not in ['yes', 'no']:
                print("Invalid input. Please enter 'yes' or 'no'.")
                value = input(f"Is {feature[3:]} available? (yes/no): ").strip().lower()
            user_data[feature] = 1 if value == 'yes' else 0

        elif feature in ['num_rooms', 'num_people', 'num_children']:  # Handle integer inputs
            value = input(f"Enter {feature.replace('_', ' ')} (integer): ").strip()
            while not value.isdigit():
                print("Invalid input. Please enter an integer.")
                value = input(f"Enter {feature.replace('_', ' ')} (integer): ").strip()
            user_data[feature] = int(value)

        elif feature == 'housearea' or feature == 'ave_monthly_income':  # Handle float inputs
            label = "house area in square meters" if feature == 'housearea' else "average monthly income in USD"
            value = input(f"Enter {label} (numeric): ").strip()
            while True:
                try:
                    user_data[feature] = float(value)
                    break
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")
                    value = input(f"Enter {label} (numeric): ").strip()

    return pd.DataFrame([user_data])

# ----------------------------------------------
# Function to Predict Electricity Generation
# ----------------------------------------------
def predict_electricity_generation(user_input_df, model_path="electricity_generation_model.pkl"):
    """
    Predict electricity generation using a pre-trained model.
    Args:
        user_input_df: DataFrame with user input.
        model_path: Path to the pre-trained model.
    Returns:
        Predicted electricity generation.
    """
    model = joblib.load(model_path)
    prediction = model.predict(user_input_df)[0]*10
    return prediction

# ----------------------------------------------
# Function to Fetch Weather Data from OpenWeatherMap API
# ----------------------------------------------
def fetch_weather_data(location, api_key):
    """
    Fetch weather data from OpenWeatherMap API for the given location.
    Args:
        location (str): City or location name.
        api_key (str): OpenWeatherMap API key.
    Returns:
        dict: Processed weather data.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error fetching weather data: {response.json().get('message', 'Unknown error')}")

    data = response.json()
    current_time = datetime.utcnow()
    solar_noon_distance = abs((current_time.hour + current_time.minute / 60) - 12) / 10

    sky_cover_mapping = {
        "clear sky": 0, "few clouds": 1, "scattered clouds": 2,
        "broken clouds": 3, "overcast clouds": 4, "mist": 5,
        "rain": 6, "snow": 7
    }
    sky_cover = data["weather"][0]["description"]
    sky_cover_numeric = sky_cover_mapping.get(sky_cover, 8)

    weather_data = {
        "Day of Year": current_time.timetuple().tm_yday,
        "Year": current_time.year,
        "Month": current_time.month,
        "Day": current_time.day,
        "First Hour of Period": current_time.hour,
        "Is Daylight": data["sys"].get("sunrise", 0) < current_time.timestamp() < data["sys"].get("sunset", 0),
        "Distance to Solar Noon": solar_noon_distance,
        "Average Temperature (Day)": (data["main"].get("temp", None) * 9/5) + 32,  # Convert to Fahrenheit
        "Average Wind Direction (Day)": data["wind"].get("deg", None),
        "Average Wind Speed (Day)": data["wind"].get("speed", None),
        "Sky Cover": sky_cover_numeric,
        "Visibility": data.get("visibility", None) / 1000,  # Convert to km
        "Relative Humidity": data["main"].get("humidity", None),
        "Average Barometric Pressure (Period)": data["main"].get("pressure", None),
    }
    return weather_data

# ----------------------------------------------
# Function to Predict Solar Power Generation
# ----------------------------------------------
def predict_solar_power(weather_data, model_path="solar_power_model.pkl"):
    """
    Predict solar power generation using a pre-trained model and weather data.
    """
    model = joblib.load(model_path)
    input_df = pd.DataFrame([weather_data])
    prediction = model.predict(input_df)[0]
    return prediction

# ----------------------------------------------
# Main Function: Guide User Through Predictions and Cost Comparison
# ----------------------------------------------
def main():
    """
    Main function to interact with the user, predict electricity and solar power,
    and provide a cost comparison.
    """
    print("\n--- Welcome to the Energy Cost Predictor ---\n")

    # User input for electricity generation prediction
    print("\nStep 1: Predict Electricity Generation\n")
    user_input_df = get_user_input()
    predicted_electricity = predict_electricity_generation(user_input_df)
    print(f"\nPredicted Electricity Generated: {(predicted_electricity):.2f} kWh")

    # Fetch weather data for solar power prediction
    print("\nStep 2: Predict Solar Power Generation\n")
    API_KEY = "c23c65adaed66dc6797af520696719ec"
    location = input("Enter your location (city name): ").strip()

    try:
        weather_data = fetch_weather_data(location, API_KEY)
        predicted_solar_power = predict_solar_power(weather_data)
        print(f"\nPredicted Solar Power Generation: {predicted_solar_power:.2f} kW")
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return

    # Step 3: Compare costs
    compare_cost(predicted_electricity, predicted_solar_power)

# ----------------------------------------------
# Run the Main Function
# ----------------------------------------------
main()
