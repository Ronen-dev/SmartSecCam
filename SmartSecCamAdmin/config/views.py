import wifi
from wifi import Cell, Scheme
from django.shortcuts import render
from django.http import Http404

import os

from crypt import crypt
from getpass import getpass
from subprocess import Popen, PIPE
# import subprocess, crypt, random, getpass



# method not for view
def Search():
    wifilist = []

    cells = Cell.all('wlan0')

    for cell in cells:
        wifilist.append(cell)

    return wifilist


def FindFromSearchList(ssid):
    wifilist = Search()

    for cell in wifilist:
        if cell.ssid == ssid:
            return cell

    return False


def FindFromSavedList(ssid):
    cell = wifi.Scheme.find('wlan0', ssid)

    if cell:
        return cell

    return False


def Connect(ssid, password=None):
    cell = FindFromSearchList(ssid)

    if cell:
        savedcell = FindFromSavedList(cell.ssid)

        # Already Saved from Setting
        if savedcell:
            savedcell.activate()
            return cell

        # First time to conenct
        else:
            if cell.encrypted:
                if password:
                    scheme = Add(cell, password)

                    try:
                        scheme.activate()

                    # Wrong Password
                    except wifi.exceptions.ConnectionError:
                        Delete(ssid)
                        return False

                    return cell
                else:
                    return False
            else:
                scheme = Add(cell)

                try:
                    scheme.activate()
                except wifi.exceptions.ConnectionError:
                    Delete(ssid)
                    return False

                return cell

    return False


def Add(cell, password=None):
    if not cell:
        return False

    scheme = wifi.Scheme.for_cell('wlan0', cell.ssid, cell, password)
    scheme.save()
    return scheme


def Delete(ssid):
    if not ssid:
        return False

    cell = FindFromSavedList(ssid)

    if cell:
        cell.delete()
        return True

    return False

#end method



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

    if request.method == "GET":

        context = { 'wifilist': Search() }

        return render(request, 'config/wifi.html', context)

    else:

        context = { 'list' : request.POST.get('wifi_name', "")}
        return render(request, 'config/wifi.html', context)
