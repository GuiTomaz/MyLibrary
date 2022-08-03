from django.contrib import admin

# Register your models here.
from .models import Planos

class PlanosAdmin(admin.ModelAdmin):
    fields = ('gratuidade', 'nome', 'preco', 'conta', 'vantagens')
    list_display = ['nome', 'gratuidade', 'preco', 'conta', 'vantagens']
    search_fields = ['nome']
admin.site.register(Planos, PlanosAdmin)