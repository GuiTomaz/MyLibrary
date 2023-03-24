# Generated by Django 3.0.2 on 2020-03-19 19:07

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categoria', '0001_initial'),
        ('produto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='data_cadastro',
            field=models.DateField(default=datetime.date(2020, 3, 19)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produto',
            name='descricao',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='produto',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='produtos', to='categoria.Categoria'),
        ),
    ]
