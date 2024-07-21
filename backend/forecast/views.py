import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from forecast.forms import CityForm
from forecast.utils import get_forecast, get_daily_forecast, \
    get_hourly_forecast


def index(request):
    """Главная страница."""

    form = CityForm(request.POST or None)
    searched_cities = request.session.get('searched_cities', [])

    if form.is_valid():
        city = form.cleaned_data['city']

        if city not in searched_cities:
            searched_cities.append(city)
        request.session['searched_cities'] = searched_cities

        return redirect(reverse('forecast:detailed_forecast',
                                kwargs={'city': city}))

    context = {
        'form': form,
        'searched_cities': searched_cities[-settings.SAVED_CITIES:],
    }
    return render(request, 'forecast/index.html', context)


def detailed_forecast(request, city):
    """Страница с детальным прогнозом погоды."""

    forecast_storage = {}

    forecast = get_forecast(city)
    if forecast:
        forecast_storage = forecast

    hourly_forecast = get_hourly_forecast(forecast_storage)
    daily_forecast = get_daily_forecast(forecast_storage)

    context = {
        'city': city.capitalize() if city else None,
        'forecast': forecast if forecast else None,
        'daily_forecast': daily_forecast if daily_forecast else None,
        'hourly_forecast': hourly_forecast if hourly_forecast else None,
    }

    return render(request, 'forecast/detailed_forecast.html', context)


def autocomplete(request):
    """Автодополнение названия города при поиске."""

    term = request.GET.get('term', '')
    file_path = os.path.join(
        os.path.dirname(__file__), '..', 'files', 'cities.txt'
    )
    file = os.path.abspath(file_path)

    with open(file, 'r', encoding='utf-8') as f:
        cities = [line.strip() for line in f]

    filtered_cities = [
        city for city in cities if city.lower().startswith(term.lower())
    ]

    return JsonResponse(filtered_cities, safe=False)
