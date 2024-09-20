
# from dotenv import load_dotenv
# import streamlit as st
# import os
# from geopy.geocoders import Nominatim
# from geopy.distance import geodesic
# import requests

# # Load environment variables
# load_dotenv()
# WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# # Initialize geolocator
# geolocator = Nominatim(user_agent="geoapiExercises")

# # Function to fetch current weather conditions and temperature for a location
# def get_weather(location):
#     url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}"
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             weather_condition = data['current']['condition']['text']
#             temperature = data['current']['temp_c']
#             return weather_condition, temperature, data['location']['lat'], data['location']['lon']
#         else:
#             st.error(f"Failed to fetch weather data. Status Code: {response.status_code}")
#             return None, None, None, None
#     except Exception as e:
#         st.error(f"Failed to fetch weather data: {e}")
#         return None, None, None, None

# # Function to calculate distance between two locations using geopy
# def calculate_distance(source_coords, destination_coords):
#     try:
#         distance = geodesic(source_coords, destination_coords).kilometers
#         return distance
#     except Exception as e:
#         st.error(f"Error in calculating distance: {e}")
#         return None

# # Function to determine the best delivery method based on weather
# def determine_delivery_method(weather_condition, temperature):
#     # Simple rules: if severe weather or high temperature, prefer sea; otherwise, air
#     if "storm" in weather_condition.lower() or temperature > 30:
#         return "Sea"
#     else:
#         return "Air"

# # Streamlit app
# st.title("Shipment Planner")

# # Input fields for source and destination
# source = st.text_input("Enter Source Location:", placeholder="Enter a city or address")
# destination = st.text_input("Enter Destination Location:",placeholder= "Enter a city or address")

# if st.button("Calculate Delivery Method"):
#     # Fetch weather data for both source and destination
#     source_weather, source_temp, source_lat, source_lon = get_weather(source)
#     dest_weather, dest_temp, dest_lat, dest_lon = get_weather(destination)

#     if source_weather and dest_weather:
#         st.write(f"Source Weather: {source_weather}, Temperature: {source_temp}°C")
#         st.write(f"Destination Weather: {dest_weather}, Temperature: {dest_temp}°C")
        
#         # Calculate distance between source and destination
#         source_coords = (source_lat, source_lon)
#         destination_coords = (dest_lat, dest_lon)
#         distance = calculate_distance(source_coords, destination_coords)
#         st.write(f"Distance: {distance:.2f} km")

#         # Determine delivery method based on source weather
#         method = determine_delivery_method(source_weather, source_temp)
#         st.write(f"Recommended Delivery Method: {method}")
#     else:
#         st.error("Error fetching weather data. Please try again.")





# from dotenv import load_dotenv
# import streamlit as st
# import os
# import google.generativeai as genai
# import requests
# from geopy.distance import geodesic

# # Load environment variables
# load_dotenv()

# # Configure the Gemini API
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Function to fetch current weather data
# def get_weather_data(location):
#     api_key = os.getenv('WEATHER_API_KEY')
#     api_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
#     try:
#         response = requests.get(api_url)
#         response.raise_for_status()
#         return response.json()
#     except requests.RequestException as e:
#         st.error(f"Error fetching weather data: {e}")
#         return None

# # Function to determine the delivery method using Gemini AI
# def determine_delivery_method(weather_data):
#     prompt = f"""
#     The current weather is {weather_data['current']['condition']['text']} with a temperature of {weather_data['current']['temp_c']}°C.
#     Based on this, should we use air or sea for delivery?
#     """
#     generation_config = {
#         "temperature": 1,
#   "top_p": 0.95,
#   "top_k": 64,
#   "max_output_tokens": 8192,
#   "response_mime_type": "text/plain",
#     }
#     try:
#         response = genai.generate_text(
#             model="gemini-1.5-flash",
#             prompt=prompt,
#             **generation_config
#         )
#         decision = response.result.strip().lower()
#         print(decision)
#         return "air" if "air" in decision else "sea"
#     except Exception as e:
#         st.error(f"An error occurred while processing the request: {e}")
#         return "air"

# # Function to calculate the distance between two locations
# def calculate_distance(source_coords, destination_coords):
#     try:
#         return geodesic(source_coords, destination_coords).kilometers
#     except Exception as e:
#         st.error(f"Error in calculating distance: {e}")
#         return None

# # Function to calculate delivery time and cost based on the delivery method
# def calculate_delivery_time_and_cost(method):
#     if method == "air":
#         days = 2
#         cost_per_day = 100
#     else:
#         days = 7
#         cost_per_day = 50
#     total_cost = days * cost_per_day
#     return days, total_cost

# # Function to handle the overall delivery method calculation
# def handle_delivery(source, destination):
#     # Fetch weather data for source and destination
#     weather_data_source = get_weather_data(source)
#     weather_data_destination = get_weather_data(destination)

#     if weather_data_source and weather_data_destination:
#         # Determine delivery method for source and destination
#         delivery_method_source = determine_delivery_method(weather_data_source)
#         delivery_method_destination = determine_delivery_method(weather_data_destination)

#         # Choose source weather for delivery method (simplification)
#         delivery_method = delivery_method_source

#         # Calculate distance
#         source_coords = (weather_data_source['location']['lat'], weather_data_source['location']['lon'])
#         destination_coords = (weather_data_destination['location']['lat'], weather_data_destination['location']['lon'])
#         distance = calculate_distance(source_coords, destination_coords)

#         if distance is not None:
#             # Calculate delivery time and cost
#             days, cost = calculate_delivery_time_and_cost(delivery_method)

#             return {
#                 "delivery_method": delivery_method,
#                 "days": days,
#                 "cost": cost,
#                 "distance": distance,
#                 "source_weather": weather_data_source['current']['condition']['text'],
#                 "source_temp": weather_data_source['current']['temp_c'],
#                 "destination_weather": weather_data_destination['current']['condition']['text'],
#                 "destination_temp": weather_data_destination['current']['temp_c'],
#             }
#     else:
#         return None

# # Streamlit app for UI
# def main():
#     st.title('Shipment Planner Based On Weather Report')

#     # Input fields for source and destination locations
#     source = st.text_input('Enter the source location:')
#     destination = st.text_input('Enter the destination location:')

#     if st.button('Calculate'):
#         if source and destination:
#             result = handle_delivery(source, destination)

#             if result:
#                 # Display results
#                 st.subheader("Delivery Details")
#                 st.write(f"**Source Weather:** {result['source_weather']}, Temperature: {result['source_temp']}°C")
#                 st.write(f"**Destination Weather:** {result['destination_weather']}, Temperature: {result['destination_temp']}°C")
#                 st.write(f"**Delivery Method:** {result['delivery_method'].capitalize()}")
#                 st.write(f"**Delivery Time:** {result['days']} days")
#                 st.write(f"**Delivery Cost:** ${result['cost']}")
#                 st.write(f"**Distance Between Source and Destination:** {result['distance']:.2f} km")
#             else:
#                 st.error("Unable to calculate delivery details. Please try again.")
#         else:
#             st.error("Please enter valid source and destination locations.")

# if __name__ == "__main__":
#     main()







from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import requests
from geopy.distance import geodesic

# Load environment variables
load_dotenv()

# Configure the Google Generative AI SDK
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set up the generation configuration for the Gemini model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 50,
  
}

# Function to fetch current weather data
def get_weather_data(location):
    api_key = os.getenv('WEATHER_API_KEY')
    api_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching weather data for {location}: {e}")
        return None

# Function to determine the delivery method using Google Gemini AI
def determine_delivery_method(weather_data):
    prompt = f"""
    The current weather is {weather_data['current']['condition']['text']} with a temperature of {weather_data['current']['temp_c']}°C.
    If the weather condition includes rain, storms, or snow, prefer sea delivery. If the temperature is above 30°C, prefer air delivery.
    Based on this, should we use air or sea for delivery?
    """

    try:
        # Create the model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        # Start a chat session
        chat_session = model.start_chat(history=[])

        # Send the prompt to the model
        response = chat_session.send_message(prompt)

        # Extract the decision from the model's response
        decision = response.text.strip().lower()

        # Return "air" or "sea" based on the model's response
        if "air" in decision:
            return "air"
        elif "sea" in decision:
            return "sea"
        else:
            return "sea"  # Default to sea if the response is unclear
    except Exception as e:
        st.warning(f"An error occurred with the AI model request: {e}")
        return "sea"  # Default to sea if an error occurs

# Function to calculate the distance between two locations
def calculate_distance(source_coords, destination_coords):
    try:
        return geodesic(source_coords, destination_coords).kilometers
    except Exception as e:
        st.error(f"Error calculating distance: {e}")
        return None

# Function to calculate delivery time and cost based on the delivery method
def calculate_delivery_time_and_cost(method):
    if method == "air":
        days = 2
        cost_per_day = 100
    else:
        days = 7
        cost_per_day = 50
    total_cost = days * cost_per_day
    return days, total_cost

# Function to handle the overall delivery method calculation
def handle_delivery(source, destination):
    # Fetch weather data for source and destination
    weather_data_source = get_weather_data(source)
    weather_data_destination = get_weather_data(destination)

    if weather_data_source and weather_data_destination:
        # Determine delivery method for source and destination
        delivery_method_source = determine_delivery_method(weather_data_source)
        delivery_method_destination = determine_delivery_method(weather_data_destination)

        # Choose source weather for delivery method (simplification)
        delivery_method = delivery_method_source

        # Calculate distance
        source_coords = (weather_data_source['location']['lat'], weather_data_source['location']['lon'])
        destination_coords = (weather_data_destination['location']['lat'], weather_data_destination['location']['lon'])
        distance = calculate_distance(source_coords, destination_coords)

        if distance is not None:
            # Calculate delivery time and cost
            days, cost = calculate_delivery_time_and_cost(delivery_method)

            return {
                "delivery_method": delivery_method,
                "days": days,
                "cost": cost,
                "distance": distance,
                "source_weather": weather_data_source['current']['condition']['text'],
                "source_temp": weather_data_source['current']['temp_c'],
                "destination_weather": weather_data_destination['current']['condition']['text'],
                "destination_temp": weather_data_destination['current']['temp_c'],
            }
    else:
        return None

# Streamlit app for UI
def main():
    st.title('Shipment Planner: Optimizing Delivery Based on Weather Conditions')

    # Input fields for source and destination locations
    source = st.text_input('Enter the source location:')
    destination = st.text_input('Enter the destination location:')

    if st.button('Calculate'):
        if source and destination:
# Function call to handle the delivery calculation process
            result = handle_delivery(source, destination)

            if result:
                # Display results
                st.subheader("Delivery Details")
                st.write(f"**Source Weather:** {result['source_weather']}, Temperature: {result['source_temp']}°C")
                st.write(f"**Destination Weather:** {result['destination_weather']}, Temperature: {result['destination_temp']}°C")
                st.write(f"**Delivery Method:** {result['delivery_method'].capitalize()}")
                st.write(f"**Delivery Time:** {result['days']} days")
                st.write(f"**Delivery Cost:** ${result['cost']}")
                st.write(f"**Distance Between Source and Destination:** {result['distance']:.2f} km")
            else:
                st.error("Unable to calculate delivery details. Please try again.")
        else:
            st.error("Please enter valid source and destination locations.")

if __name__ == "__main__":
    main()
