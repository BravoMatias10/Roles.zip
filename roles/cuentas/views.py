from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Producto
from .forms import ProductoForm, ProductoVendedorForm


def obtener_rol(usuario):
    # El superusuario es el administrador del sistema
    if usuario.is_superuser:
        return 'Administrador'
    # Revisamos si pertenece al grupo Vendedor
    if usuario.groups.filter(name='Vendedor').exists():
        return 'Vendedor'
    # El administrador asigna el rol a las cuentas nuevas
    return 'sin rol'


@login_required
def inicio(request):
    rol = obtener_rol(request.user)
    if rol not in ['Administrador', 'Vendedor']:
        return render(request, 'cuentas/403.html', {'rol': rol}, status=403)

    productos = Producto.objects.all()
    return render(request, 'cuentas/inicio.html', {
        'rol': rol,
        'productos': productos
    })


@login_required
def crear_producto(request):
    rol = obtener_rol(request.user)
    # Solo el administrador puede crear productos
    if rol != 'Administrador':
        return render(request, 'cuentas/403.html', {'rol': rol}, status=403)

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = ProductoForm()

    return render(request, 'cuentas/producto_form.html', {
        'rol': rol,
        'form': form,
        'titulo': 'Crear producto'
    })


@login_required
def editar_producto(request, pk):
    rol = obtener_rol(request.user)
    if rol not in ['Administrador', 'Vendedor']:
        return render(request, 'cuentas/403.html', {'rol': rol}, status=403)

    producto = get_object_or_404(Producto, pk=pk)
    # El vendedor solo puede editar los productos que tiene asignados
    if rol == 'Vendedor' and producto.encargado != request.user:
        return render(request, 'cuentas/403.html', {'rol': rol}, status=403)

    # El formulario del vendedor no permite cambiar el encargado
    if rol == 'Administrador':
        formulario = ProductoForm
    else:
        formulario = ProductoVendedorForm

    if request.method == 'POST':
        form = formulario(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = formulario(instance=producto)

    return render(request, 'cuentas/producto_form.html', {
        'rol': rol,
        'form': form,
        'titulo': 'Editar producto'
    })


@login_required
def eliminar_producto(request, pk):
    rol = obtener_rol(request.user)
    # Solo el administrador puede eliminar productos
    if rol != 'Administrador':
        return render(request, 'cuentas/403.html', {'rol': rol}, status=403)

    producto = get_object_or_404(Producto, pk=pk)
    # Primero mostramos la confirmación y después eliminamos
    if request.method == 'POST':
        producto.delete()
        return redirect('inicio')

    return render(request, 'cuentas/producto_confirmar_eliminar.html', {
        'rol': rol,
        'producto': producto
    })
