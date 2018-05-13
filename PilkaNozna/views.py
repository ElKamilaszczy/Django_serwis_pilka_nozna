from django.shortcuts import render
from django.http import HttpResponse
from .models import Liga
from .forms import PostForm
from django.shortcuts import redirect

def ligi(request):
    latest_question = Liga.objects.order_by('nazwa_ligi')

    context = {'latest_question': latest_question}
    return render(request, 'PilkaNozna/base.html', context)

def detail(request, id_ligi):
    return HttpResponse("You're looking at question %s." % id_ligi)


def add_liga(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = True)
            post.save()

    else:
        form = PostForm()
    return render(request, 'PilkaNozna/index1.html', {'form': form})



