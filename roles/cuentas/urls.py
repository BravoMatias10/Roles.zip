from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='cuentas/login.html',
                                   redirect_authenticated_user=True), name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('', views.inicio, name='inicio'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
]
