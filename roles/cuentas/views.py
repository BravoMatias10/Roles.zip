from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProductoForm, ProductoVendedorForm
from .models import Producto


def obtener_rol(usuario):
    if usuario.is_superuser:
        return 'Administrador'
    if usuario.groups.filter(name='Vendedor').exists():
        return 'Vendedor'
    return 'Sin rol'


def denegado(request, rol):
    return render(request, 'cuentas/403.html', {'rol': rol}, status=403)


@login_required
def inicio(request):
    rol = obtener_rol(request.user)
    if rol == 'Sin rol':
        return denegado(request, rol)
    productos = Producto.objects.select_related('encargado').all()
    return render(request, 'cuentas/inicio.html', {'rol': rol, 'productos': productos})


@login_required
def crear_producto(request):
    rol = obtener_rol(request.user)
    if rol != 'Administrador':
        return denegado(request, rol)
    form = ProductoForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Producto creado.')
        return redirect('inicio')
    return render(request, 'cuentas/producto_form.html', {
        'rol': rol, 'form': form, 'titulo': 'Crear producto'})


@login_required
def editar_producto(request, pk):
    rol = obtener_rol(request.user)
    if rol == 'Sin rol':
        return denegado(request, rol)
    producto = get_object_or_404(Producto, pk=pk)
    if rol != 'Administrador' and producto.encargado_id != request.user.pk:
        return denegado(request, rol)
    formulario = ProductoForm if rol == 'Administrador' else ProductoVendedorForm
    form = formulario(request.POST if request.method == 'POST' else None, instance=producto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Producto actualizado.')
        return redirect('inicio')
    return render(request, 'cuentas/producto_form.html', {
        'rol': rol, 'form': form, 'titulo': 'Editar producto'})


@login_required
def eliminar_producto(request, pk):
    rol = obtener_rol(request.user)
    if rol != 'Administrador':
        return denegado(request, rol)
    producto = get_object_or_404(Producto, pk=pk)
    # GET solo muestra la confirmación; únicamente POST elimina.
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado.')
        return redirect('inicio')
    return render(request, 'cuentas/producto_confirmar_eliminar.html', {
        'rol': rol, 'producto': producto})


@require_POST
def cerrar_sesion(request):
    logout(request)
    return redirect('login')
