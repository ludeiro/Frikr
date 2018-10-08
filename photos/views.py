# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from photos.models import Photo, PUBLIC


def home(request):
    """
    Controlador Home de mi página
    :param request: HttpRequest
    :return:
    """
    # Filtramos las fotos por visibilidad
    #Recuperamos fotos en orden inverso a la fecha de creación -
    photos = Photo.objects.filter(visibility=PUBLIC).order_by('-created_at')
    context = {
        'photos_list': photos[:5]
    }

    return HttpResponse(render(request, "photos/home.html", context))


def detail(request, pk):
    """
    Carga la página de detalle de una foto
    :param request:
    :param pk:
    :return:
    """
    possible_photos = Photo.objects.filter(pk=pk)
    photo = possible_photos[0] if len(possible_photos) > 0 else None
    if photo is not None:
        # cargar la plantilla de detalle
        context = {
            'photo': photo
        }
        return HttpResponse(render(request, "photos/detail.html", context))
    else:
        return HttpResponseNotFound('No existe la foto')  # 404 not found
