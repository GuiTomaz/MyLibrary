from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def ajuda(request):
    return render(request, 'ajuda.html')

def notfound(request):
    return render(request, 'notfound.html')