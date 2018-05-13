from django.shortcuts import render
from django.http import HttpResponse
from .models import Liga,Klub
from .forms import PostForm
from django.shortcuts import redirect

def ligi(request):
    latest_question = Liga.objects.order_by('nazwa_ligi')

    context = {'latest_question': latest_question}
    return render(request, 'PilkaNozna/index.html', context)

def detail(request, id_ligi):
    lg = Liga.objects.get(id_ligi=id_ligi)
    kl = Klub.objects.filter(id_ligi=id_ligi)
    context = {'lg': lg,'kl':kl}
    return render(request, 'PilkaNozna/detail.html', context)


def add_liga(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = True)
            post.save()

    else:
        form = PostForm()
    return render(request, 'PilkaNozna/index1.html', {'form': form})



