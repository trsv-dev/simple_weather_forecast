from http import HTTPStatus

import requests
from django.test import TestCase, Client
from django.urls import reverse


class ViewsTestCase(TestCase):
    """Тестируем вьюхи."""

    def setUp(self):
        """Тестовые данные."""

        self.guest_client = Client()
        self.city = 'Москва'
        self.forecast_url = 'https://api.open-meteo.com/v1/forecast'
        self.city_coords_url = 'https://geocoding-api.open-meteo.com/v1/search'

    def tearDown(self):
        """Удаляем тестовые данные после прохождения тестов."""

        pass

    def test_index_page(self):
        """Тестируем доступность главной страницы."""

        response = self.guest_client.get(reverse('forecast:index'))
        self.assertEqual(response.status_code,
                         HTTPStatus.OK,
                         msg='Главная страница недоступна!')

    def test_detailed_forecast_page(self):
        """Тестируем страницу детального прогноза."""

        response = self.guest_client.get(
            reverse('forecast:detailed_forecast', args=[self.city])
        )
        self.assertEqual(response.status_code,
                         HTTPStatus.OK,
                         msg='Страница детального прогноза недоступна!')

    def test_forecast_api_response(self):
        """Тестируем доступность API прогноза погоды."""

        response = requests.get(self.forecast_url)
        self.assertEqual(response.status_code,
                         HTTPStatus.OK,
                         msg='API прогноза погоды недоступно!')

    def test_coords_api_response(self):
        """Тестируем доступность API получения координат."""

        params = {'name': self.city}
        response = requests.get(self.city_coords_url, params=params)

        self.assertEqual(response.status_code, HTTPStatus.OK,
                         msg='API получения координат недоступно!')
