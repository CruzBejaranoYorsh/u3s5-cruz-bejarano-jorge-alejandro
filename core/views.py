from django.shortcuts import render
from .models import Servicio


def servicios(request):
    lista_servicios = Servicio.objects.all()
    return render(request, 'core/servicios.html', {'servicios': lista_servicios})