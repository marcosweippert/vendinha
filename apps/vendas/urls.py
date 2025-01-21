# urls.py
from django.urls import path
from . import views

app_name = 'vendas'

urlpatterns = [
    path('venda/<int:produto_id>/', views.realizar_venda, name='realizar_venda'),
    path('pdv/', views.pdv, name='pdv'),
    path('pdv/<int:produto_id>/', views.pdv, name='pdv_produto'),
    path('limpar_carrinho/', views.limpar_carrinho, name='limpar_carrinho'),
    path('vendas/cancelar_item/', views.cancelar_item, name='cancelar_item'),

]
