"""Ejecutar con: python manage.py shell < cargar_demo.py"""
from django.contrib.auth.models import Group, User
from cuentas.models import Producto

# Solo crea lo que falta: repetir este archivo no borra ni restablece datos.
grupo, _ = Group.objects.get_or_create(name='Vendedor')
admin, nuevo = User.objects.get_or_create(username='admin')
if nuevo:
    admin.is_superuser = True
    admin.is_staff = True
    admin.set_password('Admin12345!')
    admin.save()
for nombre in ['vendedor1', 'vendedor2']:
    usuario, nuevo = User.objects.get_or_create(username=nombre)
    if nuevo:
        usuario.set_password('Vendedor12345!')
        usuario.save()
    usuario.groups.add(grupo)
v1 = User.objects.get(username='vendedor1')
v2 = User.objects.get(username='vendedor2')
for nombre, precio, stock, encargado in [
    ('Arroz 1 kg', 1500, 20, v1), ('Leche 1 litro', 1200, 15, v1),
    ('Pan de molde', 2200, 10, v2), ('Aceite 1 litro', 2500, 12, v2)]:
    Producto.objects.get_or_create(nombre=nombre, defaults={
        'precio': precio, 'stock': stock, 'encargado': encargado})
print('Datos de demostración disponibles.')
