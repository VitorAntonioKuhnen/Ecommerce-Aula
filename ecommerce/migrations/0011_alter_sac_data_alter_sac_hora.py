# Generated by Django 4.1.2 on 2022-12-07 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0010_hist_produto_tamanho'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sac',
            name='data',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='sac',
            name='hora',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
