from django.urls import path
from planos import views

app_name = 'planos'

urlpatterns=[
    path('lista_planos', views.lista_planos, name='lista_planos')
]