# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout


def login(request):
    pass


def logout(request):
    if request.user.is_authenticated():
        django_logout(request)
    return redirect('photos_home')
