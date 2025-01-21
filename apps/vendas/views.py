from django.shortcuts import render, get_object_or_404
from .models import Vendas
from apps.produtos.models import Produtos
from django.http import HttpResponse
from django.http import JsonResponse
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q


# Create your views here.
def realizar_venda(request, produto_id):
    produto = Produtos.objects.get(id=produto_id)
    quantidade = int(request.GET.get('quantidade', 1))
    venda = Vendas.objects.create(produto=produto, quantidade=quantidade)
    produto.estoque -= quantidade
    produto.save()
    return HttpResponse(f'Venda realizada! Total: R${venda.total}')



def pdv(request):
    # Se o carrinho já existe na sessão, recuperamos ele
    if 'carrinho' not in request.session:
        request.session['carrinho'] = []

    # Garantir que o contador de itens esteja sempre na sessão
    if 'item_counter' not in request.session:
        request.session['item_counter'] = 0  # Inicializa o contador se não existir

    carrinho = request.session['carrinho']
    item_counter = request.session['item_counter']

    # Calcular o total, garantindo que a soma seja feita com Decimal
    total = sum(Decimal(item['total']) for item in carrinho)

    # Variável para armazenar o query de pesquisa
    search_query = request.GET.get('search', '').strip()
    produto = None
    erro_busca = False

    if search_query:
        # Busca pelo código do produto com o código exato ou parte do nome
        produto = Produtos.objects.filter(
            Q(codigo__icontains=search_query) | Q(nome__icontains=search_query)
        )
        if not produto.exists():
            erro_busca = True  # Marca que não encontrou nenhum produto correspondente
    else:
        erro_busca = True  # Caso o campo de busca esteja vazio, marca como erro

    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        
        # Verificar se produto_id não é vazio ou inválido
        if not produto_id or not produto_id.isdigit():
            return redirect('vendas:pdv')  # Redireciona se produto_id estiver inválido ou vazio

        produto_id = int(produto_id)  # Converte para inteiro

        quantidade = request.POST.get('quantidade', 1)  # Por padrão 1
        peso = request.POST.get('peso', 0)  # Por padrão 0

        try:
            quantidade = int(quantidade)  # Converter para inteiro
        except ValueError:
            quantidade = 1  # Se der erro, atribui 1

        try:
            peso = float(peso)  # Converter para float, pois pode ser número decimal
        except ValueError:
            peso = 0  # Se der erro, atribui 0

        # Usando get_object_or_404 para garantir que o produto seja encontrado corretamente
        produto = get_object_or_404(Produtos, id=produto_id)

        # Se o produto for cobrado por kg
        if produto.categoria == 'Frios' and peso > 0:
            preco_total = produto.preco * Decimal(peso / 1000)  # Divide por 1000 para converter gramas para kg
        else:
            preco_total = produto.preco * Decimal(quantidade)  # Produto por unidade, convertendo para Decimal

        # Incrementa o contador para gerar um id único para este item
        item_counter += 1
        request.session['item_counter'] = item_counter  # Atualiza o contador de itens na sessão

        item = {
            'id': item_counter,
            'produto_id': produto.id,
            'nome': produto.nome,
            'quantidade': quantidade if peso == 0 else peso,
            'preco_unitario': float(produto.preco),
            'total': float(preco_total),
            'peso': peso
        }

        # Adiciona o produto ao carrinho
        carrinho.append(item)

        # Converte todos os valores de 'Decimal' para 'float' antes de armazenar na sessão
        for item in carrinho:
            item['total'] = float(item['total'])
            item['preco_unitario'] = float(item['preco_unitario'])

        request.session['carrinho'] = carrinho

        return redirect('vendas:pdv')

    return render(request, 'vendas/pdv.html', {
        'produto': produto,
        'carrinho': carrinho,
        'total': total,
        'search_query': search_query,
        'erro_busca': erro_busca
    })




def limpar_carrinho(request):
    # Limpar o carrinho na sessão
    if 'carrinho' in request.session:
        del request.session['carrinho']
        del request.session['item_counter']
    
    return redirect('vendas:pdv')  # Redireciona de volta para a página PDV

def cancelar_item(request):
    carrinho = request.session.get('carrinho', [])

    # Obter o item_id do formulário POST
    item_id = request.POST.get('item_id')

    # Encontrar o item no carrinho baseado no id
    item = next((item for item in carrinho if item['id'] == int(item_id)), None)

    if item:
        # Subtrair o valor do item cancelado do total
        total = sum(float(item['total']) for item in carrinho)  # Converte para float para evitar o erro de serialização

        # Criar um novo item para representar o item cancelado
        item_counter = len(carrinho) + 1  # Pega o contador do carrinho para o novo item
        cancelado_item = {
            'id': item_counter,  # ID único para o item cancelado
            'nome': f"{item['nome']} - CANCELADO",  # Nome do item com a indicação de cancelado
            'quantidade': item['quantidade'],
            'preco_unitario': -float(item['preco_unitario']),  # Preço negativo
            'total': -float(item['total']),  # Total negativo
            'peso': item['peso'],
            'cancelado': True  # Marca este item como cancelado
        }

        # Adicionar o item cancelado ao carrinho
        carrinho.append(cancelado_item)

        # Atualiza o carrinho na sessão com o item cancelado
        request.session['carrinho'] = carrinho

        # Atualiza o total após o cancelamento (subtraindo o valor cancelado)
        request.session['total'] = total - float(item['total'])  # Subtrai o valor do item cancelado

    return redirect('vendas:pdv')  # Redireciona de volta para o PDV




