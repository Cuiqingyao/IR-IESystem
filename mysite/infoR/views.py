from django.shortcuts import render, HttpResponse

# Create your views here.


def index(request):
    return HttpResponse('hello world')

def search(request):
    pass

def detail(request):
    pass