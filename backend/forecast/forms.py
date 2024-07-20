from django import forms
from django.core.validators import RegexValidator


class CityForm(forms.Form):
    city = forms.CharField(
        label='Город',
        max_length=200,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zА-Яа-я\s-]+$',
                message='Введите допустимое название города '
                        '(только буквы, дефисы и пробелы)'
            )
        ]
    )
