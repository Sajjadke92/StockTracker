from django.shortcuts import render
from django.http import HttpResponse


from .models import Category,Item

def Category_list(request):
    warehouses = Category.objects.all()
    context = {'warehouses': warehouses}
    return render(request, 'warehouses/Category_list.html',context = context)

def Category_detail(request,Category_id):
    warehouses = Category.objects.get(pk=Category_id)
    context = {'warehouses':warehouses}
    return render(request,'warehouses/Category_detail.html',context=context)


def home(request):
    return HttpResponse('<h1> welcome to StockTracker </h1>')