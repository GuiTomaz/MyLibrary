from django.db import models

# Create your models here.
class Planos(models.Model):
    gratuidade = models.CharField(max_length=100, blank=True)
    nome = models.CharField(max_length=70, db_index=True, unique=True)
    preco = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    conta = models.CharField(max_length=100, blank=True)
    vantagens = models.CharField(max_length=1000, blank=True)

    class Meta:
        db_table='planos'
        ordering=('nome',)

    def __str__(self):
        return self.nome