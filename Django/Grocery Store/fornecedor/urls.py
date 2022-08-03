from django.urls import path

from fornecedor import views

app_name = 'fornecedor'

urlpatterns = [
    path('lista_fornecedor/', views.lista_fornecedor, name='lista_fornecedor'),
    path('cadastra_fornecedor/', views.cadastra_fornecedor, name='cadastra_fornecedor'),
    path('exibe_fornecedor/<int:id>', views.exibe_fornecedor, name='exibe_fornecedor'),
    path('edita_fornecedor/<int:id>', views.edita_fornecedor, name='edita_fornecedor'),
    path('remove_fornecedor/', views.remove_fornecedor, name='remove_fornecedor')
]