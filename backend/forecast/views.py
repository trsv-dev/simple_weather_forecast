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
        'searched_cities': searched_cities,
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
