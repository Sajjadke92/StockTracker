from django.shortcuts import render


from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1> welcome to StockTracker </h1>')