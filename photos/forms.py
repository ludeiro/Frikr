# -*- coding:_utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from photos.models import Photo
from photos.settings import BADWORDS


class PhotoForm(forms.ModelForm):
    """"
    Formulario para el modelo Photo
    """
    class Meta:
        model = Photo
        exclude = ['owner']

    def clean(self):
        """
        Valida si en la descripción se han puesto tacos definidos en settings.BADWORDS
        :return: Diccionario con los diccionarios si OK
        """
        cleaned_data = super(PhotoForm, self).clean()

        description = cleaned_data.get('description', '')

        for badword in BADWORDS:
            if badword.lower() in description.lower():
                raise ValidationError(u'La palabra {0} no está permitida'.format(badword))

        return cleaned_data

