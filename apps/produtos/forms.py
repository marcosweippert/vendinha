from django import forms
from .models import Produtos

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produtos
        fields = ['codigo', 'nome', 'categoria', 'descricao', 'preco', 'preco_custo', 'estoque']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }
