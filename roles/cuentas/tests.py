from django.contrib.auth.models import Group, User
from django.test import TestCase, Client
from .models import Producto


class PermisosTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', '', 'clave12345')
        grupo = Group.objects.create(name='Vendedor')
        self.vendedor = User.objects.create_user('vendedor', password='clave12345')
        self.otro = User.objects.create_user('otro', password='clave12345')
        self.sinrol = User.objects.create_user('sinrol', password='clave12345')
        self.vendedor.groups.add(grupo)
        self.otro.groups.add(grupo)
        self.producto = Producto.objects.create(nombre='Arroz', precio=1500, stock=10,
                                              encargado=self.vendedor)
        self.editar = f'/productos/{self.producto.pk}/editar/'
        self.eliminar = f'/productos/{self.producto.pk}/eliminar/'
        self.datos = {'nombre': 'Leche', 'precio': '1200', 'stock': 8,
                      'encargado': self.vendedor.pk}

    def test_anonimo(self):
        for url in ['/', '/productos/crear/', self.editar, self.eliminar]:
            for metodo in [self.client.get, self.client.post]:
                self.assertEqual(metodo(url).status_code, 302)

    def test_login_logout(self):
        self.assertRedirects(self.client.post('/login/',
            {'username': 'vendedor', 'password': 'clave12345'}), '/')
        self.assertEqual(self.client.get('/logout/').status_code, 405)
        self.assertRedirects(self.client.post('/logout/'), '/login/')

    def test_admin_crud(self):
        self.client.force_login(self.admin)
        self.assertContains(self.client.get('/'), 'Arroz')
        self.assertEqual(self.client.get('/productos/crear/').status_code, 200)
        self.assertRedirects(self.client.post('/productos/crear/', self.datos), '/')
        self.assertTrue(Producto.objects.filter(nombre='Leche').exists())
        self.assertEqual(self.client.get(self.editar).status_code, 200)
        self.assertRedirects(self.client.post(self.editar, self.datos), '/')
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Leche')
        self.assertEqual(self.client.get(self.eliminar).status_code, 200)
        self.assertTrue(Producto.objects.filter(pk=self.producto.pk).exists())
        self.assertRedirects(self.client.post(self.eliminar), '/')
        self.assertFalse(Producto.objects.filter(pk=self.producto.pk).exists())

    def test_vendedor_edita_solo_propios_y_no_reasigna(self):
        self.client.force_login(self.vendedor)
        self.assertContains(self.client.get('/'), 'Arroz')
        self.assertEqual(self.client.get(self.editar).status_code, 200)
        self.datos['encargado'] = self.otro.pk
        self.assertRedirects(self.client.post(self.editar, self.datos), '/')
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Leche')
        self.assertEqual(self.producto.encargado, self.vendedor)
        self.client.force_login(self.otro)
        for metodo in [self.client.get, self.client.post]:
            self.assertEqual(metodo(self.editar, self.datos).status_code, 403)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.encargado, self.vendedor)

    def test_vendedor_no_crea_ni_elimina(self):
        self.client.force_login(self.vendedor)
        for url in ['/productos/crear/', self.eliminar]:
            for metodo in [self.client.get, self.client.post]:
                self.assertEqual(metodo(url, self.datos).status_code, 403)
        self.assertEqual(Producto.objects.count(), 1)

    def test_sin_rol(self):
        self.client.force_login(self.sinrol)
        for url in ['/', '/productos/crear/', self.editar, self.eliminar]:
            for metodo in [self.client.get, self.client.post]:
                self.assertEqual(metodo(url, self.datos).status_code, 403)

    def test_validacion(self):
        self.client.force_login(self.admin)
        for cambios in [{'precio': '-1'}, {'stock': '-1'}, {'nombre': ''},
                        {'encargado': self.sinrol.pk}]:
            datos = dict(self.datos, **cambios)
            self.assertEqual(self.client.post('/productos/crear/', datos).status_code, 200)
        self.assertEqual(Producto.objects.count(), 1)

    def test_csrf(self):
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.admin)
        self.assertEqual(cliente.post('/productos/crear/', self.datos).status_code, 403)
