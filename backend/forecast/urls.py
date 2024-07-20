from django.urls import path

from forecast import views

app_name = 'forecast'

urlpatterns = [
    path('', views.index, name='index'),
    path('detailed_forecast/<str:city>/',
         views.detailed_forecast, name='detailed_forecast'),
]
