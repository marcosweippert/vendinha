# apps/vendas/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def format_currency(value):
    """
    Formata o valor para o formato monetário brasileiro (R$ 1.250,00).
    """
    try:
        # Certifique-se de que o valor é um número flutuante
        value = float(value)
        # Formata o número para o estilo brasileiro de moeda
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return value  # Retorna o valor original se ocorrer algum erro
