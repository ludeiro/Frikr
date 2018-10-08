# -*- coding: utf-8 -*-

from django import forms

class LoginForm(forms.Form):

    usr = forms.CharField(label='Nombre de usuario')
    pwd = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
