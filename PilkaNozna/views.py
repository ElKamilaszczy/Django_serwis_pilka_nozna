from django.shortcuts import render
from django.http import HttpResponse
from .models import Liga,Klub,Mecz,Pilkarz,Statystyki_gracza
from .forms import PostForm
from operator import itemgetter
from django.shortcuts import redirect

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
    pomoc = 0
    for a in kl:

        mecz = Mecz.objects.filter(id_klubu1=a.id_klubu) | Mecz.objects.filter(id_klubu2=a.id_klubu)
        for b in range (9):
            if b==0:
                abc[var][b]=var

            if b==1:
                abc[var][b]=a
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
        id.insert(pomoc, a.id_klubu)
        pomoc += 1

        var += 1

    abc = sorted(abc, key=lambda x: x[3], reverse=True)
    pomocnicza = 0
    miejsce = 1
    for a in kl:
        if(abc[pomocnicza][3] == abc[pomocnicza+1][3]):
            abc[pomocnicza][0] = miejsce

        else:
            abc[pomocnicza][0] = miejsce
            miejsce += 1

        pomocnicza += 1
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
    '''
    wsk = 1;
    lg = Liga.objects.get(id_ligi=id_ligi)
    kl = Klub.objects.filter(id_ligi=id_ligi)
    abc = [[0 for j in range(100)] for i in range(100)]
    var = 1
    pilkarz = Pilkarz.objects
    #MUSI BYC TUTAJ COS O PILKARZU#
    for a in kl:
        pilkarz = Pilkarz.objects.filter(id_klubu=a.id_klubu)
        for c in pilkarz:
            for b in range (4):
                if b==0:
                    abc[var][b]=var
                if b==1:
                    abc[var][b] = (c.imie + ' ' + c.nazwisko)
                if b==2:
                    abc[var][b] = a.nazwa_klubu
                if b==3:
                    abc[var][b] = gole_zawodnika(c.id_pilkarza, c.id_klubu)


                    var += 1
                    continue
    context = {'lg': lg, 'kl': kl, 'abc': abc, 'wsk': wsk}
    return render(request, 'PilkaNozna/detail.html', context)
    '''
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
    kl = Klub.objects.get(id_klubu = id_klubu, id_ligi = lg)
    context = {'lg': lg, 'kl':kl}
    return render(request, 'PilkaNozna/klub.html', context)

def add_liga(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = True)

    else:
        form = PostForm()
    return render(request, 'PilkaNozna/index1.html', {'form': form})



