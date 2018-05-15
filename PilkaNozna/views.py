from django.shortcuts import render
from django.http import HttpResponse
from .models import Liga,Klub,Mecz
from .forms import PostForm
from django.shortcuts import redirect



def ligi(request):
    latest_question = Liga.objects.order_by('nazwa_ligi')

    context = {'latest_question': latest_question}
    return render(request, 'PilkaNozna/index.html', context)

def detail(request, id_ligi):
    lg = Liga.objects.get(id_ligi=id_ligi)
    kl = Klub.objects.filter(id_ligi=id_ligi)
    abc = [[0 for j in range(100)] for i in range(100)]
    var = 1
    for a in kl:

        mecz = Mecz.objects.filter(id_klubu1=a.id_klubu) | Mecz.objects.filter(id_klubu2=a.id_klubu)

        for b in range (8):
            if b==0:
                abc[var][b]=var

            if b==1:
                abc[var][b]=a.nazwa_klubu
            if b==2:
                abc[var][b]=mecz.count()





        var += 1




    context = {'lg': lg,'kl':kl,'abc':abc,'mecz':mecz}
    return render(request, 'PilkaNozna/detail.html', context)


def add_liga(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = True)

    else:
        form = PostForm()
    return render(request, 'PilkaNozna/index1.html', {'form': form})



