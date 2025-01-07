from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponseNotFound,HttpRequest
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from .models import Category,Item
from .forms import CategoryForm,ItemForm


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
    items = Item.objects.filter(Category = warehouses).order_by('quantity')

    #prepare data for chart
    labels = [item.name for item in items]
    quantities = [item.quantity for item in items]

    context = {'warehouses':warehouses,'items':items,'labels':labels,'quantities':quantities}
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

def Add_item(request,Category_id):
    try:
        category = Category.objects.get(pk= Category_id)
    except Category.DoesNotExist:
        return HttpResponseNotFound() 
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
           Item.objects.create(Category=category,**form.cleaned_data)
           return HttpResponseRedirect(f'/warehouses/{Category_id}/')
    else:
        form = ItemForm()     

    return render(request,'warehouses/Add_item.html',{'form':form,'category':category})   

def Item_chart(request):
    
    items = Item.objects.all().order_by('quantity')
    labels = [item.name for item in items] 
    quantities = [item.quantity for item in items]

    context = {'labels':labels , 'quantities':quantities}
    
    return render(request,'warehouses/Item_chart.html',context=context)

def update_item(request,Category_id, Item_id):
    item = get_object_or_404(Item, id=Item_id, Category_id=Category_id)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance =item)
        if form.is_valid():
            updated_item = form.save()
            # Check if the quantity is below the threshold
            if updated_item.quantity< 5:
                send_notification(updated_item)
            return HttpResponseRedirect(f'/warehouses/{item.Category.pk}')
    else:
        form = ItemForm(instance = item)

    return render(request,'warehouses/update_item.html',{'form':form, 'item':item})    

def delete_item(request, Category_id, Item_id):
    item = get_object_or_404(Item, id=Item_id, Category_id=Category_id)

    if request.method == "POST":
        item.delete()
        return redirect('Category_detail', Category_id=Category_id)

    return render(request, 'warehouses/confirm_delete.html', {'item': item, 'Category_id': Category_id})

def home(request):
    #return HttpResponse('<h1> welcome to StockTracker </h1>')
    return render(request,'warehouses/home.html' )

def send_notification(item):
    subject = f"Low Stock Alert: {item.name}"
    message = f"The stock for item '{item.name}' is below the threshold. Current quantity: {item.quantity}."
    from_email = 'django@mailtrap.club'
    recipient_list = ['test.mailtrap1234@gmail.com']  # Add the recipient email here

    send_mail(subject, message, from_email, recipient_list)

def expiry_check(request):
    # Calculate the date one month from now
    one_month_later = now().date()+timedelta(days=30)
    # Filter items with expiry date less than one month away
    expiring_items = Item.objects.filter(expiry__lte = one_month_later).order_by('expiry')
    context={'expiring_items':expiring_items}
    return render(request,'warehouses/expiry_check.html',context=context)

def search(request):
    query=request.GET.get('q') # Get the search query from the URL
    results = []
    if query:
        # Perform a case-insensitive search on the 'name' field
        results= Item.objects.filter(name__icontains=query)
    return render(request,'warehouses/search.html',{'results': results,'query': query})

def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'warehouses/item_detail.html', {'item': item})