from django.shortcuts import render


def index(request):
    context = {
        'test': request,
    }
    return render(request, 'config/index.html', context)


def wifi(request):
    context = {}
    return render(request, 'config/wifi.html', context)
