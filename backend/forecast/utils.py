import locale
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import List, Union

import requests
from django.conf import settings
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim

logger = logging.getLogger('django')
FORECAST_URL = 'https://api.open-meteo.com/v1/forecast'

DIRECTIONS = {
    (0, 22.5): 'Север',
    (22.5, 67.5): 'Северо-Восток',
    (67.5, 112.5): 'Восток',
    (112.5, 157.5): 'Юго-Восток',
    (157.5, 202.5): 'Юг',
    (202.5, 247.5): 'Юго-Запад',
    (247.5, 292.5): 'Запад',
    (292.5, 337.5): 'Северо-Запад',
    (337.5, 360): 'Север'
}


def retries_async(max_attempts):
    """
    Параметрический декоратор для асинхронных функций. Служит для повторения
    попыток соединения с сервером указанное в параметрах декоратора
    количество раз.

    :param max_attempts: Максимальное количество попыток.
    """

    def outer_wrapper(func):
        @wraps(func)
        async def inner_wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception:
                    attempts += 1
                    logger.warning(f'Функция {func.__name__}. Попытка '
                                   f'{attempts} не удалась. Повторяем...')
                    if attempts >= max_attempts:
                        raise
        return inner_wrapper
    return outer_wrapper


@retries_async(10)
async def get_coords(city):
    """Получаем координаты города для прогноза."""

    async with Nominatim(user_agent='city_coords_app',
                         adapter_factory=AioHTTPAdapter) as geolocator:
        location = await geolocator.geocode(city, language='RU')

        if location:
            try:
                latitude = location.latitude
                longitude = location.longitude
            except AttributeError:
                latitude, longitude = 0, 0

        else:
            latitude, longitude = 0, 0

    return latitude, longitude


def convert_windspeed(windspeed: Union[float, List[float]]) -> Union[
    float, List[float]]:
    """
    Конвертируем скорость ветра из км/ч в м/с и округляем до
    одного знака после запятой.
    """

    kmh_to_ms_factor = 3.6
    if isinstance(windspeed, float):
        return round((windspeed / kmh_to_ms_factor), 1)
    elif isinstance(windspeed, list):
        return [round((speed / kmh_to_ms_factor), 1) for speed in windspeed]
    else:
        raise TypeError('Функция конвертации принимает либо float, '
                        'либо list[float]')


def get_wind_direction(degrees):
    """
    Переводит числовое значение направления ветра в текстовое направление.
    """

    for (start, end), direction in DIRECTIONS.items():
        if start <= degrees < end or (start == 0 and degrees == 360):
            return direction
    return 'Неизвестно'


async def get_forecast(city):
    """Получение прогноза для выбранного города."""

    latitude, longitude = await get_coords(city)
    if not (latitude and longitude):
        return None

    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current_weather': True,
        'hourly': ['temperature_2m', 'windspeed_10m', 'precipitation',
                   'relative_humidity_2m'],
        'forecast_days': settings.DAYS_IN_FORECAST,
        'daily': ['temperature_2m_max', 'temperature_2m_min',
                  'precipitation_sum', 'windspeed_10m_max'],
        'timezone': 'Europe/Moscow'
    }
    response = requests.get(FORECAST_URL, params=params).json()

    if 'current_weather' in response:
        current_weather = response['current_weather']
        current_weather['windspeed'] = (
            convert_windspeed(current_weather['windspeed']))
        current_weather['winddirection'] = (
            get_wind_direction(current_weather['winddirection']))
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
    windspeeds = convert_windspeed(hourly.get('windspeed_10m', []))
    precipitations = hourly.get('precipitation', [])
    relative_humidity = hourly.get('relative_humidity_2m', [])
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
                precipitations[i],
                relative_humidity[i]
            ))

    return filtered_hourly_forecast


def get_daily_forecast(forecast_storage):
    """Получение прогноза на несколько дней."""

    if not forecast_storage:
        return None

    daily = forecast_storage.get('daily', {})

    # Для представления даты в виде DD.MM
    months_and_days = [
        f'{date[8:10]}.{date[5:7]}' for date in daily.get('time', [])
    ]

    daily_forecast = zip(
        months_and_days,
        daily.get('temperature_2m_max', []),
        daily.get('temperature_2m_min', []),
        daily.get('precipitation_sum', []),
        convert_windspeed(daily.get('windspeed_10m_max', []))
    )

    return daily_forecast
