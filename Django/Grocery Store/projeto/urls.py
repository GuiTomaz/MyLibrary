from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from projeto import views, settings

urlpatterns = [
    path('', views.index, name="index"),
    path('produto/', include('produto.urls')),
    path('fornecedor/', include('fornecedor.urls')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     Como acessar a página index.html do projeto:
#     http://127.0.0.1:8000/
#
#     Como acessar a página index.html de produto:
#     http://127.0.0.1:8000/produto/