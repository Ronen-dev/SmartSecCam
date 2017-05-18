from django.shortcuts import render
import os


def index(request):
    context = {}

    # POST case
    if request.method == 'POST':

        password = request.POST.get('password', '')
        filename = '.pwd'

        # Si le mot de passe est déjà défini
        if os.path.getsize('.pwd') > 0:
            context['error'] = "Un mot de passe est déjà défini."

            return render()
        # Sinon
        else:
            file = open(filename, "w")
            file.write(password)
            file.close()

            context['success'] = "Mot de passe correctement modifié : " + password

            return render(request, 'config/wifi.html', context)

    # GET case
    else:
        return render(request, 'config/index.html', context)


def wifi(request):
    context = {}
    return render(request, 'config/wifi.html', context)
