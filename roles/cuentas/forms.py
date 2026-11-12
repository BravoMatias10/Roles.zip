from django import forms
from django.contrib.auth.models import User
from .models import Producto


class ProductoForm(forms.ModelForm):
    # Solo se pueden asignar productos a vendedores activos
    encargado = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True, groups__name='Vendedor')
    )
    precio = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)

    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock', 'encargado']


class ProductoVendedorForm(forms.ModelForm):
    precio = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)

    class Meta:
        model = Producto
        # El vendedor no puede cambiar el encargado
        fields = ['nombre', 'precio', 'stock']
