from django.shortcuts import render
from django.http import HttpResponse
from .models import Liga
from .models import Klub
# Create your views here.

#def index(request):
#    return render(request, 'PilkaNozna/index.html', { } )

def kluby(request):
    latest_question = Klub.objects.order_by('nazwa_klubu')[:5]

    context = {'latest_question': latest_question}
    return render(request, 'PilkaNozna/index.html', context)

def detail(request, id_klubu):
    return HttpResponse("You're looking at question %s." % id_klubu)



