from django.shortcuts import render, redirect
import os


def index(request):
    if request.method == 'POST':
        context = {
            'test': request.POST.get('password', '')
        }

        filename = '.pwd'

        if os.path.getsize('.pwd') > 0:
            context['error'] = "Un mot de passe est déjà défini."
        else:
            file = open(filename, "w")
            file.write(request.POST.get('password', ''))
            file.close()

            context['success'] = "Mot de passe correctement modifié: " + request.POST.get('password', '')

            # return render(request, 'config/wifi.html', context)
            return redirect('wifi/', )
    else:
        context = {
            'test': "GET OK"
        }
    return render(request, 'config/index.html', context)


def wifi(request):
    context = {}
    return render(request, 'config/wifi.html', context)
