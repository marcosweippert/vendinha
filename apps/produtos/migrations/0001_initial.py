# Generated by Django 5.1.5 on 2025-01-21 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100)),
                ('nome', models.CharField(max_length=100)),
                ('categoria', models.CharField(choices=[('Cereais', 'Cereais'), ('Geleias', 'Geleias'), ('Frios', 'Frios'), ('Massas', 'Massas')], max_length=100)),
                ('descricao', models.TextField()),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('preco_custo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estoque', models.PositiveIntegerField()),
            ],
        ),
    ]
