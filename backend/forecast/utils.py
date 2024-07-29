import locale
from datetime import datetime, timedelta

import requests

from django.conf import settings

FORECAST_URL = 'https://api.open-meteo.com/v1/forecast'
CITY_COORDS_URL = 'https://geocoding-api.open-meteo.com/v1/search'


def get_latitude(response):
    """Получаем широту города."""

    results = response.get('results', [])
    if results:
        return results[0].get('latitude')
    return None


def get_longitude(response):
    """Получаем долготу города."""

    results = response.get('results', [])
    if results:
        return results[0].get('longitude')
    return None


def get_coords(city):
    """Получаем координаты города для прогноза."""

    params = {
        'name': city,
        'count': 10,
        'format': 'json',
        'language': 'ru'
    }

    response = requests.get(CITY_COORDS_URL, params=params).json()

    latitude = get_latitude(response)
    longitude = get_longitude(response)

    return latitude, longitude


def get_forecast(city):
    """Получение прогноза для выбранного города."""

    latitude, longitude = get_coords(city)
    if not (latitude and longitude):
        return None

    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current_weather': True,
        'hourly': ['temperature_2m', 'windspeed_10m', 'precipitation'],
        'forecast_days': settings.DAYS_IN_FORECAST,
        'daily': ['temperature_2m_max', 'temperature_2m_min',
                  'precipitation_sum', 'windspeed_10m_max'],
        'timezone': 'Europe/Moscow'
    }

    response = requests.get(FORECAST_URL, params=params).json()

    if 'current_weather' in response:
        current_weather = response['current_weather']
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        current_weather_time = datetime.fromisoformat(
            current_weather.get("time").replace('Z', settings.GMT))
        current_weather['time'] = current_weather_time.strftime(
            '%d %B %Y, %H:%M:%S')

    return response


def get_hourly_forecast(forecast_storage):
    """Почасовой прогноз начиная с текущего момента."""

    if not forecast_storage:
        return None

    hourly = forecast_storage.get('hourly', {})

    times = hourly.get('time', [])
    temperatures = hourly.get('temperature_2m', [])
    windspeeds = hourly.get('windspeed_10m', [])
    precipitations = hourly.get('precipitation', [])

    current_time = datetime.now()
    end_time = current_time + timedelta(hours=settings.DAYS_IN_FORECAST)

    filtered_hourly_forecast = []
    for i, time_str in enumerate(times):
        time_dt = datetime.fromisoformat(time_str.replace('Z', settings.GMT))
        if current_time <= time_dt <= end_time:
            filtered_hourly_forecast.append((
                time_dt.strftime('%H:%M'),
                temperatures[i],
                windspeeds[i],
                precipitations[i]
            ))

    return filtered_hourly_forecast


def get_daily_forecast(forecast_storage):
    """Получение прогноза на несколько дней."""

    if not forecast_storage:
        return None

    daily = forecast_storage.get('daily', {})

    # Для представления даты в виде MM.DD
    months_and_days = [
        date.replace('-', '.')[5:] for date in daily.get('time', [])
    ]

    daily_forecast = zip(
        months_and_days,
        daily.get('temperature_2m_max', []),
        daily.get('temperature_2m_min', []),
        daily.get('precipitation_sum', []),
        daily.get('windspeed_10m_max', [])
    )

    return daily_forecast
