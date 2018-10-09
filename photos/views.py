# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from photos.forms import PhotoForm
from photos.models import Photo, PUBLIC
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.db.models import Q

class HomeView(View):

    def get(self,request):
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

class DetailView(View):

    def get(self, request, pk):
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


class CreateView(View):

    @method_decorator(login_required())
    def get(self, request):
        """"
        Muestra un formulario para crear una foto.
         :param request: HttpRequest
         :return: HttpResponse
        """
        form = PhotoForm()
        context = {
            'form': form,
            'success_message': ''
        }
        return render(request, 'photos/new_photo.html', context)

    @method_decorator(login_required())
    def post(self, request):
        """"
         Crea una foto en base a la información POST
         :param request: HttpRequest
         :return: HttpResponse
        """
        success_message = ''
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

class ListView(View):

    def get(self, request):
        """
        Devuelve:
         - Las fotos publicas si el usuario no esta autenticado.
         - Las fotos del usuario autenticado o las públicas de otros.
         - Si el usuario es administrador => Todas las fotos
        :param request: HttpRequest
        :return: HttpResponse
        """

        if not request.user.is_authenticated:  # Si no está autenticado
            photos = Photo.objects.filter(visibility=PUBLIC)
        elif request.user.is_superuser:  # Si es administrador
            photos = Photo.objects.all()
        else:
            photos = Photo.objects.filter(Q(owner=request.user) | Q(visibility=PUBLIC))

        context = {
            'photos': photos
        }

        return render(request, 'photos/photos_list.html', context)
