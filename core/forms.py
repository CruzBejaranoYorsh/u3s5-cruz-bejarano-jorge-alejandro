# forms: trae las herramientas de Django para construir formularios
from django import forms
# ValidationError: la excepción que Django usa para reportar un error de validación
from django.core.exceptions import ValidationError
# Servicio: el modelo de la Unidad 2, importado desde este mismo directorio
from .models import Servicio


# ServicioForm: el mismo ModelForm del paso 01, ahora con una regla extra
class ServicioForm(forms.ModelForm):
    # Meta: configuración del formulario (de qué modelo sale y qué campos muestra)
    class Meta:
        # model: el formulario se genera a partir del modelo Servicio
        model = Servicio
        # fields: los campos que aparecen en el formulario, en este orden
        fields = ['titulo', 'descripcion', 'precio', 'categoria']

    # clean_precio: Django lo llama automáticamente al validar el campo "precio"
    def clean_precio(self):
        # self.cleaned_data: diccionario con los valores ya convertidos a su tipo de Python
        precio = self.cleaned_data['precio']
        # regla propia: rechazar precios en cero o negativos, algo que DecimalField no revisa solo
        if precio <= 0:
            # ValidationError: si se dispara, el formulario se considera inválido y muestra este mensaje
            raise ValidationError('El precio debe ser mayor a 0.')
        # si no se disparó el error, hay que devolver el valor limpio para que el formulario lo use
        return precio
