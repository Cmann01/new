import tkinter as tk
import requests

API_KEY = 'e40c683930ad798a5cb3d855f3995c95'  # Replace with your OpenWeatherMap API key
UNITS = 'metric'  # Default to Celsius

# Function to fetch weather data from the OpenWeatherMap API
def fetch_weather(city_name, units=UNITS):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city_name, 'appid': API_KEY, 'units': units}

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data['cod'] == 200:
            temperature = data['main']['temp']
            description = data['weather'][0]['description']
            update_result_label(f'Temperature: {temperature}°{units}\nWeather: {description}')
        else:
            update_result_label(f'City not found. ({data["message"]})')

    except requests.ConnectionError:
        update_result_label('Connection Error')
    except requests.RequestException as e:
        update_result_label(f'Error: {str(e)}')

# Function to update the result label
def update_result_label(text):
    result_label.config(text=text)

# Create the main window
app = tk.Tk()
app.title('Weather App')

# Create and configure widgets
city_label = tk.Label(app, text='Enter City:')
city_label.pack()

city_entry = tk.Entry(app)
city_entry.pack()

unit_var = tk.StringVar()
unit_var.set(UNITS)  # Default unit
unit_frame = tk.Frame(app)
unit_frame.pack()

celsius_radio = tk.Radiobutton(unit_frame, text='Celsius', variable=unit_var, value='metric')
celsius_radio.pack(side='left')
fahrenheit_radio = tk.Radiobutton(unit_frame, text='Fahrenheit', variable=unit_var, value='imperial')
fahrenheit_radio.pack(side='left')

get_weather_button = tk.Button(app, text='Get Weather', command=lambda: fetch_weather(city_entry.get(), unit_var.get()))
get_weather_button.pack()

result_label = tk.Label(app, text='', wraplength=300)  # Wrap text after 300 pixels
result_label.pack()

# Start the GUI application
app.mainloop()
