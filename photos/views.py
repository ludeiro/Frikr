# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from photos.forms import PhotoForm
from photos.models import Photo, PUBLIC
from django.contrib.auth.decorators import login_required


def home(request):
    """
    Controlador Home de mi página
    :param request: HttpRequest
    :return:
    """
    #  Filtramos las fotos por visibilidad
    #  Recuperamos fotos en orden inverso a la fecha de creación -
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
    possible_photos = Photo.objects.filter(pk=pk).select_related('owner')
    photo = possible_photos[0] if len(possible_photos) > 0 else None
    if photo is not None:
        # cargar la plantilla de detalle
        context = {
            'photo': photo
        }
        return HttpResponse(render(request, "photos/detail.html", context))
    else:
        return HttpResponseNotFound('No existe la foto')  # 404 not found


@login_required()
def create(request):
    """"
    Muestra un formulario para crear una foto.
     :param request: HttpRequest
     :return: HttpResponse
    """
    success_message = ''
    if request.method == 'GET':
        form = PhotoForm()
    else:
        photo_with_owner = Photo()
        photo_with_owner.owner = request.user  # Propietario de la foto el usuario autenticado
        form = PhotoForm(request.POST, instance=photo_with_owner)
        if form.is_valid():
            new_photo = form.save()  # Guarda el objeto y lo devuelve
            form = PhotoForm()
            success_message = 'Guardado con éxito!'
            success_message += '<a href={0}>'.format(reverse('photo_detail', args=[new_photo.pk]))
            success_message += 'Ver foto'
            success_message += '</a>'
    context = {
        'form': form,
        'success_message': success_message
    }
    return render(request, 'photos/new_photo.html', context)
