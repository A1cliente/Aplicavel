from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('painel-cliente/', views.painel_cliente, name='painel_cliente'),
    path('painel-mototaxista/', views.painel_mototaxista, name='painel_mototaxista'),
    path('solicitar-corrida/', views.solicitar_corrida, name='solicitar_corrida'),
    path('aceitar-corrida/<int:corrida_id>/', views.aceitar_corrida, name='aceitar_corrida'),
    path('atualizar-localizacao/', views.atualizar_localizacao, name='atualizar_localizacao'),
    path('localizacao_motoboy/<str:username>/', views.localizacao_motoboy, name='localizacao_motoboy'),
    path('painel/', views.painel, name='painel'),
    path('frente_tela/', views.tela, name='tela'),
    path('fim/', views.sair, name='sair'),
]
