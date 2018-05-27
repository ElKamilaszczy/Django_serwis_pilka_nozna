from django.shortcuts import render
from django.http import HttpResponse
from .models import Liga,Klub,Mecz,Pilkarz,Statystyki_gracza
from .forms import PostForm
#Import formularza logowania
from .forms import LoginForm
#Import mechanizmów uwierzytelniania i umieszczenia w sesji (login)
from django.contrib.auth import authenticate, login
from operator import itemgetter
from django.shortcuts import redirect
#Dla zalogowanego:
from django.contrib.auth.decorators import login_required
def ligi(request):
    latest_question = Liga.objects.order_by('nazwa_ligi')

    context = {'latest_question': latest_question}
    return render(request, 'PilkaNozna/index.html', context)

def gole(id_meczu,id_klubu):
    pilkarz = Pilkarz.objects.filter(id_klubu=id_klubu)
    mecz = Mecz.objects.get(id_meczu=id_meczu)
    gole = 0
    gole_p = 0
    staty = Statystyki_gracza.objects.filter(id_meczu=id_meczu)
    if id_klubu == mecz.id_klubu1.id_klubu:
        przeciwnik = mecz.id_klubu2.id_klubu
    else:
        przeciwnik = mecz.id_klubu1.id_klubu
    pilkarz_p = Pilkarz.objects.filter(id_klubu=przeciwnik)

    for d in pilkarz:
        for e in staty:
            if e.id_pilkarza.id_pilkarza == d.id_pilkarza:
                gole += e.gole

    for d in pilkarz_p:
        for e in staty:
            if d.id_pilkarza == e.id_pilkarza.id_pilkarza:
                gole_p += e.gole

    tab = []
    tab.insert(0,gole)
    tab.insert(1,gole_p)
    return tab


def tabela(request, id_ligi):
    wsk = 0;
    lg = Liga.objects.get(id_ligi=id_ligi)
    kl = Klub.objects.filter(id_ligi=id_ligi)
    abc = [[0 for j in range(100)] for i in range(100)]
    id = [0 for j in range(100)]
    var = 0
    #pomoc = 0
    for a in kl:

        mecz = Mecz.objects.filter(id_klubu1=a.id_klubu) | Mecz.objects.filter(id_klubu2=a.id_klubu)
        for b in range (10):
            if b==0:
                abc[var][b]=var

            if b==1:
                abc[var][b]=a.nazwa_klubu
                #id.insert(var,a.id_klubu)

            if b==2:
                abc[var][b]=mecz.count()
            if b==3:
                for c in mecz:
                    temp = gole(c.id_meczu,a.id_klubu)

                    if temp[0] > temp[1]:

                        abc[var][b] += 3
                    if temp[0] == temp[1]:
                        abc[var][b] += 1

            if b==4:
                for c in mecz:
                    temp = gole(c.id_meczu,a.id_klubu)
                    if temp[0] > temp[1]:
                        abc[var][b] += 1
            if b==5:
                for c in mecz:
                    temp = gole(c.id_meczu,a.id_klubu)
                    if temp[0] < temp[1]:
                        abc[var][b] += 1
            if b==6:
                for c in mecz:
                    temp = gole(c.id_meczu,a.id_klubu)
                    if temp[0] == temp[1]:
                        abc[var][b] += 1
            if b==7:
                for c in mecz:
                    temp = gole(c.id_meczu,a.id_klubu)
                    abc[var][b] += temp[0]
            if b==8:
                for c in mecz:
                    temp = gole(c.id_meczu,a.id_klubu)
                    abc[var][b] += temp[1]
            if b==9:
                abc[var][b] = a.id_klubu
        #id.insert(pomoc, a.id_klubu)
        #pomoc += 1

        var += 1

    abc = sorted(abc, key=lambda x: x[3], reverse=True)
    pomocnicza = 0
    miejsce = 1
    for a in kl:
        if(abc[pomocnicza][3] == abc[pomocnicza+1][3]) and (abc[pomocnicza][7]-abc[pomocnicza][8]) == (abc[pomocnicza+1][7] - abc[pomocnicza+1][8]):
            abc[pomocnicza][0] = miejsce

        else:
            abc[pomocnicza][0] = miejsce
            miejsce += 1

        pomocnicza += 1
    request.session['tablica_wynikow'] = abc
    context = {'lg': lg, 'kl': kl, 'abc': abc, 'wsk': wsk, 'id': id}
    return render(request, 'PilkaNozna/detail.html', context)

#Dla wypisywania listy wszystkich strzelców bramek w danej lidze
def gole_zawodnika(id_pilkarza, id_klubu):
    pilkarz = Pilkarz.objects.filter(id_klubu=id_klubu)
    gole = 0
    staty = Statystyki_gracza.objects.filter(id_pilkarza = id_pilkarza).filter(gole__gt = 0)
    for d in pilkarz:
        for e in staty:
            if e.id_pilkarza.id_pilkarza == d.id_pilkarza:
                gole += e.gole

    return gole
def ranking_st(request, id_ligi):
    wsk = 1
    lg = Liga.objects.get(id_ligi=id_ligi)
    kl = Klub.objects.filter(id_ligi=lg)
    abc = [[0 for j in range(4)] for i in range(1000)]
    var = 0
    pilkarz = Pilkarz.objects.all()
    # MUSI BYC TUTAJ COS O PILKARZU#
    for a in kl:
        for c in pilkarz:
            if gole_zawodnika(c.id_pilkarza, a.id_klubu) == 0:
                continue
            for b in range(4):
                if b == 0:
                    abc[var][b] = var
                if b == 1:
                    abc[var][b] = (c.imie + ' ' + c.nazwisko)
                if b == 2:
                    abc[var][b] = a.nazwa_klubu
                if b == 3:
                    abc[var][b] = gole_zawodnika(c.id_pilkarza, a.id_klubu)
            var += 1
    #Próba posortowania
    abc = sorted(abc, key=lambda x: x[3], reverse=True)
    pomocnicza = 0
    miejsce = 1
    for x in range(var):
        if(abc[pomocnicza][3] == abc[pomocnicza+1][3]):
            abc[pomocnicza][0] = miejsce
        else:
             abc[pomocnicza][0] = miejsce
             miejsce += 1

        pomocnicza += 1

    context = {'lg': lg, 'pilkarz': pilkarz, 'abc': abc, 'wsk': wsk, 'var': var}
    return render(request, 'PilkaNozna/detail.html', context)

def kolejki(request,id_ligi):
    wsk=2
    lg = Liga.objects.get(id_ligi=id_ligi)
    kl = Klub.objects.filter(id_ligi=id_ligi)
    id = [0 for j in range(100)]
    var = 0
    for a in kl:
        id.insert(var,a.id_klubu)
        var+=1
    var = 0
    statystyki = Statystyki_gracza.objects.all().order_by('id_pilkarza')
    gol = [0 for j in range(100)]

    for a in statystyki:
        if a.gole!=0:
            for b in range(a.gole):
                gol[var]=a
                var+=1

    mecze = Mecz.objects.filter(id_klubu1__in=id).order_by('-kolejka','-data_meczu')
    kol=mecze[0].kolejka
    var = 1
    abc = [[0 for j in range(2)] for i in range(1000)]
    for a in mecze:
        abc[var][0] = gole(a.id_meczu,a.id_klubu1.id_klubu)[0]
        abc[var][1] = gole(a.id_meczu, a.id_klubu1.id_klubu)[1]
        var+=1

    context = {'wsk': wsk,'lg': lg,'mecze':mecze,'range':range(kol,0,-1),'abc':abc,'gol':gol,'statystyki':statystyki}
    return render(request, 'PilkaNozna/detail.html', context)

def klub(request,id_ligi,id_klubu):
    lg = Liga.objects.get(id_ligi = id_ligi)
    kl = Klub.objects.filter(id_ligi = lg, id_klubu = id_klubu)
    pilkarz1 = Pilkarz.objects.filter(id_klubu = id_klubu)
    abc = [[0 for j in range(100)] for i in range(100)]
    id = [0 for j in range(100)]
    var = 0
    #Miejsce na ogólne statystyki#
    for a in kl:
        mecz = Mecz.objects.filter(id_klubu1=a.id_klubu) | Mecz.objects.filter(id_klubu2=a.id_klubu)
        for b in range(13):
            if b == 0:
                abc[var][b] = var
            if b == 1:
                abc[var][b] = a.nazwa_klubu
            if b == 2:
                abc[var][b] = mecz.count()
            if b == 3:
                for c in mecz:
                    temp = gole(c.id_meczu, a.id_klubu)

                    if temp[0] > temp[1]:
                        abc[var][b] += 3
                    if temp[0] == temp[1]:
                        abc[var][b] += 1
            if b == 4:
                for c in mecz:
                    temp = gole(c.id_meczu, a.id_klubu)
                    if temp[0] > temp[1]:
                        abc[var][b] += 1
            if b == 5:
                for c in mecz:
                    temp = gole(c.id_meczu, a.id_klubu)
                    if temp[0] < temp[1]:
                        abc[var][b] += 1
            if b == 6:
                for c in mecz:
                    temp = gole(c.id_meczu, a.id_klubu)
                    if temp[0] == temp[1]:
                        abc[var][b] += 1
            if b == 7:
                for c in mecz:
                    temp = gole(c.id_meczu, a.id_klubu)
                    abc[var][b] += temp[0]
            if b == 8:
                for c in mecz:
                    temp = gole(c.id_meczu, a.id_klubu)
                    abc[var][b] += temp[1]
            if b == 9:
                abc[var][b] = a.id_klubu
            if b == 10:
                for c in mecz:
                    staty1 = Statystyki_gracza.objects.filter(id_meczu = c.id_meczu)
                    for s in staty1:
                        for p1 in pilkarz1:
                            if p1.id_pilkarza == s.id_pilkarza.id_pilkarza:
                                abc[var][b] += s.faule
            if b == 11:
                for c in mecz:
                    staty1 = Statystyki_gracza.objects.filter(id_meczu=c.id_meczu)
                    for s in staty1:
                        for p1 in pilkarz1:
                            if p1.id_pilkarza == s.id_pilkarza.id_pilkarza:
                                abc[var][b] += s.zolta
            if b == 12:
                for c in mecz:
                    staty1 = Statystyki_gracza.objects.filter(id_meczu=c.id_meczu)
                    for s in staty1:
                        for p1 in pilkarz1:
                            if p1.id_pilkarza == s.id_pilkarza.id_pilkarza:
                                abc[var][b] += s.czerwona
        var += 1
    abc = sorted(abc, key=lambda x: x[3], reverse=True)
    pomocnicza = 0
    miejsce = 1
    #Tutaj ogólne statystyki dla poszczególnych graczy#
    pilkarz_staty = [[0 for j in range(100)] for i in range(100)]
    pilkarz = Pilkarz.objects.filter(id_klubu = id_klubu)
    var = 0
    for p in pilkarz:
        staty = Statystyki_gracza.objects.filter(id_pilkarza = p.id_pilkarza)
        for b in range(10):
            if b == 0:
                pilkarz_staty[var][b] = p.id_pilkarza
            if b == 1:
                pilkarz_staty[var][b] = (p.imie + ' ' + p.nazwisko)
            if b == 2:
                pilkarz_staty[var][b] = p.wiek_pilkarza()
            if b == 3:
                for s in staty:
                        pilkarz_staty[var][b] = staty.count()
            if b == 4:
                for s in staty:
                        pilkarz_staty[var][b] += s.gole
            if b == 5:
                for s in staty:
                        pilkarz_staty[var][b] += s.asysty
            if b == 6:
                for s in staty:
                        pilkarz_staty[var][b] += s.faule
            if b == 7:
                for s in staty:
                        pilkarz_staty[var][b] += s.zolta
            if b == 8:
                for s in staty:
                        pilkarz_staty[var][b] += s.czerwona
            if b == 9:
                pilkarz_staty[var][b] = p.id_pozycji.nazwa_pozycji
        var += 1

    context = {'lg': lg, 'kl':kl, 'abc':abc, 'a':a, 'pilkarz_staty': pilkarz_staty, 'pilkarz': pilkarz}
    return render(request, 'PilkaNozna/klub.html', context)

def add_liga(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = True)

    else:
        form = PostForm()
    return render(request, 'PilkaNozna/index1.html', {'form': form})


'''Widok dla formularza logowania organizatora/użytkownika'''
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        request.session.set_expiry(0)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(login = cd['login'], hasło = cd['hasło'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'Pilkanozna/base.html')
                else:
                    return HttpResponse('Konto jest zablokowane')
            else:
                return HttpResponse('Nieprawidłowe dane logowania')
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'PilkaNozna/login.html', context)

'''Widok ograniczony dla zalogowanych'''
@login_required
def dashboard(request):
    return render(request, 'PilkaNozna/dashboard.html', {'section': dashboard})
