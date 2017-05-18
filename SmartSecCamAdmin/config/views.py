from django.shortcuts import render
from django.http import Http404

import os

from crypt import crypt
from getpass import getpass
from subprocess import Popen, PIPE
# import subprocess, crypt, random, getpass

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

            ####
            #                  MODIFICATION DU MOT DE PASSE
            #   COMMENTER CETTE PARTIE POUR NE PAS AVOIR UNE MAUVAISE SURPRISE !
            ####

            # sudo_password_callback = 'azerty'
            # username, username_password = 'pi', password
            #
            # try:
            #     hashed = crypt(username_password)
            # except TypeError:
            #     p = Popen(
            #         ["mkpasswd", "-m", "sha-512", "-s"],
            #         stdin=PIPE,
            #         stdout=PIPE,
            #         universal_newlines=True
            #     )
            #
            #     hashed = p.communicate(username_password)[0][:-1]
            #     assert p.wait() == 0
            # assert hashed == crypt(username_password, hashed)
            #
            # p = Popen(
            #     ['sudo', '-S', 'usermod', '-p', hashed, username],
            #     stdin=PIPE,
            #     universal_newlines=True
            # )
            #
            # p.communicate(sudo_password_callback + '\n')
            # assert p.wait() == 0

            #
            # FIN MODIFICATION MOT DE PASSE
            #

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
            context['success'] = "Connexion à votre espace réussie!"
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
