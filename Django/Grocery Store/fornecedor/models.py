from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Fornecedor(models.Model):
    nome = models.CharField(max_length=100, db_index=True, unique=True)
    slug = models.SlugField(max_length=70)
    endereco = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    cnpj = models.CharField(max_length=18, unique=True)

    class Meta:
        db_table='fornecedor'

    def __str__(self):
        return self.nome
