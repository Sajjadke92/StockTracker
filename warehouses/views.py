from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect


from .models import Category,Item
from .forms import CategoryForm


def Category_list(request):
    warehouses = Category.objects.all()
    context = {'warehouses': warehouses}
    return render(request, 'warehouses/Category_list.html',context = context)

def Category_detail(request,Category_id):
    warehouses = Category.objects.get(pk=Category_id)
    items = Item.objects.filter(Category = warehouses)
    context = {'warehouses':warehouses,'items':items}
    return render(request,'warehouses/Category_detail.html',context=context)

def Category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            Category.objects.create(**form.cleaned_data)
            return HttpResponseRedirect('/warehouses/')
    else:
        form = CategoryForm()

    return render(request,'warehouses/Category_create.html',{'form':form})


def home(request):
    return HttpResponse('<h1> welcome to StockTracker </h1>')