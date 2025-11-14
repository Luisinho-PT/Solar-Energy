from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app.views import *
urlpatterns = [
    path('admin/', admin.site.urls),

    # ROTAS DE LOGIN / LOGOUT
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registrar/', UserCreateView.as_view(), name='register'),
    path("perfil/", profile_view, name="profile"),
    path('', loja_home, name='home'),
    path('', include('app.urls')),
]
