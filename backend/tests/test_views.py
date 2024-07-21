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
        self.city_2 = 'Санкт-Петербург'
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

    def test_redirect_after_post_in_index_page(self):
        """
        Проверяем, что произошел редирект на страницу детального прогноза
        после POST-запроса на главной странице.
        """

        index_url = reverse('forecast:index')
        detailed_forecast_url = reverse('forecast:detailed_forecast',
                                        args=[self.city])

        response = self.guest_client.post(index_url, {'city': self.city})

        self.assertRedirects(response, detailed_forecast_url,
                             status_code=HTTPStatus.FOUND)

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

    def test_save_cities_in_session(self):
        """
        Тестируем сохранение в сессии городов,
        прогноз в которых запрашивал пользователь.
        """

        self.guest_client.post(reverse('forecast:index'), {'city': self.city})
        self.guest_client.post(reverse('forecast:index'), {'city': self.city_2})
        self.guest_client.session.save()

        searched_cities = self.guest_client.session.get('searched_cities', [])

        self.assertIn(
            self.city,
            searched_cities,
            'Город при поиске не добавляется в просмотренные города!'
            )

        self.assertIn(
            self.city_2,
            searched_cities,
            'Следующий город при поиске не добавляется в просмотренные города!'
        )

        self.assertTrue(
            len(self.guest_client.session['searched_cities']) == 2,
            'В сессии сохраняется неверное количество введенных ранее городов!'
        )

        self.assertTrue(
            'searched_cities' in self.guest_client.session,
            'Списка сохраняемых городов нет в сессии пользователя!'
        )
