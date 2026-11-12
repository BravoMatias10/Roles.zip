# Mi Tienda

Proyecto sencillo para la preprueba: usuarios, roles y CRUD de productos.
Usa Python 3.11, Django 3.2.25 y SQLite3. Conserva la organización del ejemplo:
`roles/manage.py`, `roles/config/`, `roles/cuentas/` y plantillas en
`roles/cuentas/templates/cuentas/`. Se añadió forms.py y una migración para el CRUD.

## Ejecutar en Windows

Abre una terminal en la carpeta `Mi Tienda` que contiene este archivo:

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
cd roles
python manage.py migrate
python manage.py runserver
```

Entra a http://127.0.0.1:8000/

En Linux/macOS, crea el entorno con `python3.11 -m venv .venv` y actívalo
con `source .venv/bin/activate`; el resto de los comandos es igual.

## Cuentas de demostración

La base db.sqlite3 ya incluye estas cuentas y cuatro productos ficticios:

| Usuario | Contraseña | Rol |
| --- | --- | --- |
| admin | Admin12345! | Administrador |
| vendedor1 | Vendedor12345! | Vendedor |
| vendedor2 | Vendedor12345! | Vendedor |

Estas credenciales y la configuración DEBUG son solo para la demostración local.

Si empiezas sin la base de datos incluida, ejecuta `python manage.py migrate` y
luego `python manage.py shell < cargar_demo.py`. Este último comando crea las
cuentas y productos que faltan, sin borrar los existentes.

## Qué puede hacer cada rol

- Administrador: listar, crear, editar, reasignar y eliminar cualquier producto.
  Su rol se identifica por `is_superuser`, igual que en el proyecto original.
- Vendedor: listar todos los productos y editar nombre, precio y stock únicamente
  de los que tiene asignados. Pertenece al grupo `Vendedor`.
- Cuenta sin rol: recibe una página 403 al acceder al catálogo o al CRUD.

Los botones cambian según el perfil, pero los permisos también se comprueban
antes de guardar datos en views.py. El formulario del vendedor no acepta el
campo encargado, aunque se envíe manualmente. Eliminar y cerrar sesión requieren
POST y los formularios incluyen CSRF. Precio y stock no pueden ser negativos.

## Demostración para la evaluación

1. Entra como admin. Crea un producto y asígnalo a vendedor1.
2. Comprueba que aparece en la lista, edítalo y elimina otro producto.
3. Cierra sesión y entra como vendedor1. Verás los cuatro productos de ejemplo,
   pero solo podrás editar Arroz y Leche, además del nuevo que le hayas asignado.
4. Copia la URL de edición de un producto de vendedor2 (por ejemplo, desde admin)
   e intenta abrirla como vendedor1: aparecerá un error 403.
5. Como vendedor, intenta abrir `/productos/crear/`: también recibirás 403.

Para agregar vendedores, entra como admin a `/admin/`, crea un usuario y asígnalo
al grupo Vendedor. Luego podrás seleccionarlo como encargado de un producto.
Para crear otro administrador usa `python manage.py createsuperuser`.

## Dónde está cada parte

- `config/settings.py`: SQLite, aplicación instalada y redirecciones de sesión.
- `config/urls.py`: enlaza cuentas y el administrador de Django.
- `cuentas/models.py`: Producto (nombre, precio, stock y encargado).
- `cuentas/forms.py`: formulario del administrador y formulario del vendedor.
- `cuentas/views.py`: CRUD, roles y validaciones de acceso.
- `cuentas/urls.py`: direcciones del login, logout y productos.
- `cuentas/templates/cuentas/`: HTML y estilos en base.html, como en el ejemplo.
- `cuentas/tests.py`: pruebas de autenticación, CRUD, permisos y validaciones.

Desde la carpeta roles, ejecuta `python manage.py test` para comprobar las pruebas.
