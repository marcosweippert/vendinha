from django.shortcuts import render, redirect
from .models import Produtos
from .forms import ProdutoForm



def produto_list(request):
    produtos = Produtos.objects.all()
    return render(request, 'produtos/produto_list.html', {'produtos': produtos})



def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produtos:produto_list')  # Redirect to the product list after saving
    else:
        form = ProdutoForm()
    return render(request, 'produtos/cadastrar_produto.html', {'form': form})
