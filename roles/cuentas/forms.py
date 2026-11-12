from decimal import Decimal
from django import forms
from django.contrib.auth.models import User
from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock', 'encargado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['precio'].min_value = Decimal('0')
        self.fields['stock'].min_value = 0
        self.fields['encargado'].queryset = User.objects.filter(
            is_active=True, groups__name='Vendedor').distinct()

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio


class ProductoVendedorForm(ProductoForm):
    class Meta(ProductoForm.Meta):
        # El vendedor no puede cambiar el encargado, ni enviándolo por POST.
        fields = ['nombre', 'precio', 'stock']

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['precio'].min_value = Decimal('0')
        self.fields['stock'].min_value = 0
