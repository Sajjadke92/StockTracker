from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound,HttpRequest

from .models import Category,Item
from .forms import CategoryForm


class GeneralView:
    def __init__(self, queryset, template_name, context_object_name):
        self.queryset = queryset
        self.template_name = template_name
        self.context_object_name = context_object_name

    def as_view(self):
        """Returns a callable function that Django can use as a view."""
        def view_function(request: HttpRequest):
            context = {self.context_object_name: self.queryset}
            return render(request, self.template_name, context)
        return view_function
    

class Categorylist(GeneralView):
    def __init__(self):
        super().__init__(
    queryset = Category.objects.all(),
    template_name = 'warehouses/Category_list.html',
    context_object_name = 'warehouses'        
    )
        
category_list_view = Categorylist().as_view()



def Category_detail(request,Category_id):
    try:
        warehouses = Category.objects.get(pk=Category_id)
    except Category.DoesNotExist:
        return HttpResponseNotFound()  
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