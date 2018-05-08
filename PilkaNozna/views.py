from django.shortcuts import render
from django.http import HttpResponse
from .models import Liga
from .models import Klub
# Create your views here.

#def index(request):
#    return render(request, 'PilkaNozna/index.html', { } )


def liga(request):
    latest_question_list = Liga.objects.order_by('nazwa_ligi')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'PilkaNozna/index.html', context)

def kluby(request):
    latest_question = Klub.objects.order_by('id_klubu')[:5]
    context = {'latest_question': latest_question}
    return render(request, 'PilkaNozna/index.html', context)
