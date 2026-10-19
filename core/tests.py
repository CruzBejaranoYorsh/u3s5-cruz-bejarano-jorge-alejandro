from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Servicio


class ServicioCrudTests(TestCase):
    def setUp(self):
        self.propietario = User.objects.create_user(
            username='propietario',
            password='test-password',
        )
        self.client.force_login(self.propietario)
        self.servicio = Servicio.objects.create(
            propietario=self.propietario,
            titulo='Servicio inicial',
            descripcion='Descripción inicial',
            precio='100.00',
            categoria='General',
        )

    def test_crear_servicio(self):
        response = self.client.post(reverse('crear_servicio'), {
            'titulo': 'Servicio nuevo',
            'descripcion': 'Descripción nueva',
            'precio': '250.50',
            'categoria': 'Diseño',
        })

        self.assertRedirects(response, reverse('servicios'))
        self.assertTrue(Servicio.objects.filter(titulo='Servicio nuevo').exists())

    def test_editar_servicio(self):
        response = self.client.post(
            reverse('editar_servicio', args=[self.servicio.pk]),
            {
                'titulo': 'Servicio actualizado',
                'descripcion': 'Descripción actualizada',
                'precio': '150.00',
                'categoria': 'Soporte',
            },
        )

        self.assertRedirects(response, reverse('servicios'))
        self.servicio.refresh_from_db()
        self.assertEqual(self.servicio.titulo, 'Servicio actualizado')

    def test_precio_debe_ser_mayor_a_cero(self):
        response = self.client.post(reverse('crear_servicio'), {
            'titulo': 'Servicio inválido',
            'descripcion': 'Descripción',
            'precio': '0',
            'categoria': 'General',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'El precio debe ser mayor a 0.')
        self.assertFalse(Servicio.objects.filter(titulo='Servicio inválido').exists())

    def test_eliminar_servicio_requiere_confirmacion_post(self):
        url = reverse('eliminar_servicio', args=[self.servicio.pk])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Servicio.objects.filter(pk=self.servicio.pk).exists())

        response = self.client.post(url)
        self.assertRedirects(response, reverse('servicios'))
        self.assertFalse(Servicio.objects.filter(pk=self.servicio.pk).exists())

    def test_crear_servicio_requiere_inicio_de_sesion(self):
        self.client.logout()

        response = self.client.get(reverse('crear_servicio'))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('crear_servicio')}",
        )

    def test_usuario_solo_ve_sus_servicios(self):
        otro_usuario = User.objects.create_user(
            username='otro_usuario',
            password='test-password',
        )
        otro_servicio = Servicio.objects.create(
            propietario=otro_usuario,
            titulo='Servicio de otra cuenta',
            descripcion='Descripción privada',
            precio='75.00',
            categoria='General',
        )

        response = self.client.get(reverse('servicios'))

        self.assertContains(response, self.servicio.titulo)
        self.assertNotContains(response, otro_servicio.titulo)

    def test_usuario_no_puede_editar_servicio_ajeno(self):
        otro_usuario = User.objects.create_user(
            username='otro_usuario',
            password='test-password',
        )
        otro_servicio = Servicio.objects.create(
            propietario=otro_usuario,
            titulo='Servicio de otra cuenta',
            descripcion='Descripción privada',
            precio='75.00',
            categoria='General',
        )

        response = self.client.post(
            reverse('editar_servicio', args=[otro_servicio.pk]),
            {
                'titulo': 'Servicio modificado',
                'descripcion': 'Descripción modificada',
                'precio': '80.00',
                'categoria': 'General',
            },
        )

        self.assertEqual(response.status_code, 404)
        otro_servicio.refresh_from_db()
        self.assertEqual(otro_servicio.titulo, 'Servicio de otra cuenta')

    def test_usuario_no_puede_eliminar_servicio_ajeno(self):
        otro_usuario = User.objects.create_user(
            username='otro_usuario',
            password='test-password',
        )
        otro_servicio = Servicio.objects.create(
            propietario=otro_usuario,
            titulo='Servicio de otra cuenta',
            descripcion='Descripción privada',
            precio='75.00',
            categoria='General',
        )

        response = self.client.post(
            reverse('eliminar_servicio', args=[otro_servicio.pk]),
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Servicio.objects.filter(pk=otro_servicio.pk).exists())
