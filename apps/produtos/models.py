from django.db import models

class Produtos(models.Model):
    codigo = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100, choices=[
        ('Cereais', 'Cereais'),
        ('Geleias', 'Geleias'),
        ('Frios', 'Frios'),
        ('Massas', 'Massas'),
        ('Bebidas', 'Bebidas'),
    ])
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField()

    def __str__(self):
        return self.nome