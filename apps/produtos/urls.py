from django.urls import path
from . import views

app_name = 'produtos'


urlpatterns = [
    path('', views.produto_list, name='produto_list'),
    path('cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),

]