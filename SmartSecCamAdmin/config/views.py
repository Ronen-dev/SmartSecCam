from django.shortcuts import render
from django.http import Http404
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

            return render(request, 'config/index.html', context)
        # Sinon
        else:
            file = open(filename, "w")
            file.write(password)
            file.close()

            context['success'] = "Mot de passe correctement modifié : " + password

            return render(request, 'config/profil.html', context)

    # GET case
    else:

        filename = '.pwd'

        # Si le mot de passe est déjà défini
        if os.path.getsize('.pwd') > 0:
            return render(request, 'config/login.html', context)
        else:
            return render(request, 'config/index.html', context)


def signin(request):
    context = {}

    if request.method != 'POST':
        raise Http404("Cette page n'existe pas.")
    else:
        password = request.POST.get('password', '')
        filename = '.pwd'

        file = open(filename, "r")
        is_correct = password == file.read()
        file.close()

        if is_correct:
            return render(request, 'config/profil.html', context)
        else:
            context['error'] = "Mot de passe saisi incorrect."
            return render(request, 'config/login.html', context)


def profiloption(request):
    context = {}

    if request.method != 'POST':
        raise Http404("Cette page n'existe pas.")
    else:
        option = request.POST.get('typeoption', '')

        if option == '1':
            return render(request, 'config/chgmdp.html', context)
        elif option == '2':
            return render(request, 'config/wifi.html', context)
        else:
            return render(request, 'config/profil.html', context)


def chgmdppost(request):
    context = {}

    if request.method != 'POST':
        raise Http404("Cette page n'existe pas.")
    else:
        password = request.POST.get('password', '')
        filename = '.pwd'

        file = open(filename, "w")
        file.write(password)
        file.close()

        context['success'] = "Votre mot de passe a bien été modifié."

        return render(request, 'config/profil.html', context)


def wifi(request):
    context = {}
    return render(request, 'config/wifi.html', context)
