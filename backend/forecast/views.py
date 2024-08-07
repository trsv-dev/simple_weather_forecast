from dadata import DadataAsync
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from forecast.forms import CityForm
from forecast.utils import get_forecast, get_daily_forecast, \
    get_hourly_forecast, retries_async


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
                                kwargs={'city': city.replace('/', '|')}))

    context = {
        'form': form,
        'searched_cities': searched_cities[-settings.SAVED_CITIES:],
    }
    return render(request, 'forecast/index.html', context)


async def detailed_forecast(request, city):
    """Страница с детальным прогнозом погоды."""

    forecast_storage = {}

    forecast = await get_forecast(city)
    if forecast:
        forecast_storage = forecast

    hourly_forecast = get_hourly_forecast(forecast_storage)
    daily_forecast = get_daily_forecast(forecast_storage)

    context = {
        'city': city if city else None,
        'forecast': forecast if forecast else None,
        'daily_forecast': daily_forecast if daily_forecast else None,
        'hourly_forecast': hourly_forecast if hourly_forecast else None,
        'latitude': forecast_storage.get('latitude', None),
        'longitude': forecast_storage.get('longitude', None),
        'yandex_api_key': settings.YANDEX_API_KEY if settings.YANDEX_API_KEY else None,
    }

    return render(request, 'forecast/detailed_forecast.html', context)


@retries_async(settings.RETRIES_QUANTITY)
async def autocomplete(request):
    """Автодополнение названия города при поиске."""

    term = request.GET.get('term', '')

    DADATA_TOKEN = settings.DADATA_TOKEN
    DADATA_SECRET = settings.DADATA_SECRET

    async with DadataAsync(DADATA_TOKEN, DADATA_SECRET) as dadata_async:
        result = await dadata_async.suggest(
            language='RU',
            name="address",
            query=term,
            from_bound={"value": "city"},
            to_bound={"value": "city"},
            locations=[
                {
                    "country_iso_code": "*"
                }
            ],
            locations_boost=[
                {"country_iso_code": "RU"}
            ]
        )

    return JsonResponse(result, safe=False)
