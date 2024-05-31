import requests
import math
from datetime import datetime
from dotenv import dotenv_values
config = dotenv_values(".env")


class WeatherData:
    LON = 20.080274
    LAT = 46.273047
    KEY = config['WEATHER_API_KEY']
    BASE_URL = 'https://api.openweathermap.org/data/2.5/'
    URL_PARAMETERS = f'?&units=metric&lang=en&lat={LAT}&lon={LON}&appid={KEY}'
    URL_WEATHER = f'{BASE_URL}weather{URL_PARAMETERS}'
    # URL_FORECAST = f'{BASE_URL}forecast{URL_PARAMETERS}'

    def __init__(self):
        self.sky_status = 'N/A'
        self.sky_icon = ''
        self.temperature = 'N/A'
        self.humidity = 'N/A'
        self.pressure = 'N/A'
        self.wind_speed = 'N/A'
        self.wind_direction = 'N/A'
        self.wind_description = 'N/A'
        self.bike_parts = []
        self.sunrise = 'N/A'
        self.sunset = 'N/A'
        self.last_update = 'N/A'
        self.is_the_sun_up = True
        self.is_it_morning = True

    def wind_to_string(self, wind_direction):
        wind = ""
        if ((337.5 < wind_direction) or (wind_direction <= 22.5)):
            wind = "North"
        elif ((22.5 < wind_direction) and (wind_direction <= 67.5)):
            wind = "Northeast"
        elif ((67.5 < wind_direction) and (wind_direction <= 112.5)):
            wind = "East"
        elif ((112.5 < wind_direction) and (wind_direction <= 157.5)):
            wind = "Southeast"
        elif ((157.5 < wind_direction) and (wind_direction <= 202.5)):
            wind = "South"
        elif ((202.5 < wind_direction) and (wind_direction <= 247.5)):
            wind = "Southwest"
        elif ((242.5 < wind_direction) and (wind_direction <= 292.5)):
            wind = "West"
        elif ((292.5 < wind_direction) and (wind_direction <= 337.5)):
            wind = "Northwest"

        wind += f' ({wind_direction}°)'
        return wind

    def classify_wind_speed(self, wind_speed):
        wind_limit = 10
        if (2*wind_limit < wind_speed):
            return (1, "Excellent", wind_speed)
        elif ((wind_limit < wind_speed) and (wind_speed <= 2*wind_limit)):
            return (2, "Good", wind_speed)
        elif ((-1*wind_limit < wind_speed) and (wind_speed <= wind_limit)):
            return (3, "Fair", wind_speed)
        elif ((-2*wind_limit < wind_speed) and (wind_speed <= -1*wind_limit)):
            return (4, "Poor", wind_speed)
        elif (wind_speed <= -2*wind_limit):
            return (5, "Bad", wind_speed)

    def calculate_bike_parts(self, is_it_morning, wind_direction, wind_speed):
        bikeparts = []
        part1 = 0
        part2 = 0

        if (is_it_morning):
            part1 = wind_speed * math.cos(math.radians(wind_direction))
            part2 = wind_speed * math.sin(math.radians(wind_direction))
            part2 *= -1
        else:
            part1 = wind_speed * math.sin(math.radians(wind_direction))
            part2 = wind_speed * math.cos(math.radians(wind_direction))
            part2 *= -1

        bikeparts.append(self.classify_wind_speed(part1))
        bikeparts.append(self.classify_wind_speed(part2))
        return bikeparts

    def update_actual_data(self):
        response = requests.get(self.URL_WEATHER)
        if response.status_code == 200:
            data = response.json()
            # Weather data
            self.sky_status = data['weather'][0]['description'].capitalize()
            self.sky_icon = "icons/sky/"+data['weather'][0]['icon']+".png"
            # Temperature, hummidiy and air pressure data
            self.temperature = data['main']['temp']
            self.pressure = data['main']['pressure']
            self.humidity = data['main']['humidity']
            # Wind data
            self.wind_speed = data['wind']['speed'] * 3.6
            self.wind_direction = data['wind']['deg']
            self.wind_description = self.wind_to_string(self.wind_direction)
            # Time data
            sunrise_time = datetime.fromtimestamp(data['sys']['sunrise'])
            self.sunrise = sunrise_time.strftime('%Y.%m.%d %H:%M')
            sunset_time = datetime.fromtimestamp(data['sys']['sunset'])
            self.sunset = sunset_time.strftime('%Y.%m.%d %H:%M')
            update_time = datetime.fromtimestamp(data['dt'])
            self.last_update = update_time.strftime('%Y.%m.%d %H:%M:%S')

            if (update_time.strftime('%H') < '12'):
                self.is_it_morning = True
            else:
                self.is_it_morning = False

            if ((update_time < sunrise_time) or (sunset_time < update_time)):
                self.is_the_sun_up = False
            else:
                self.is_the_sun_up = True

            # Bike data
            self.bike_parts = self.calculate_bike_parts(
                self.is_it_morning,
                self.wind_direction,
                self.wind_speed)

        else:
            print('Error fetching weather data')

    def update_forecast_data(self):
        response = requests.get(config['URL_FORECAST'])
        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print('Error fetching weather data')


if __name__ == '__main__':
    wd = WeatherData()
    wd.update_actual_data()
    print(wd.sky_status)
    print(wd.__dict__)
