from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponseNotFound,HttpRequest
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from .models import Category,Item
from django.forms import modelformset_factory
from .forms import CategoryForm,ItemForm,ItemQuantityForm


class GeneralView:
    """
    A reusable class-based view for rendering a queryset in a specified template.

    Attributes:
        queryset: The data to be passed to the template.
        template_name: The name of the template to be rendered.
        context_object_name: The name of the variable to be used in the template context.
    """
    def __init__(self, queryset, template_name, context_object_name):
        self.queryset = queryset
        self.template_name = template_name
        self.context_object_name = context_object_name

    def as_view(self):
        """
        Returns a callable function that Django can use as a view.
        The returned function takes an HttpRequest, prepares the context, and renders the template.
        """
        def view_function(request: HttpRequest):
            context = {self.context_object_name: self.queryset}
            return render(request, self.template_name, context)
        return view_function
    

class Categorylist(GeneralView):
    """
    A specialized view for listing all categories.

    Inherits from GeneralView and sets up specific attributes for rendering a category list.
    """
    def __init__(self):
        super().__init__(
    queryset = Category.objects.all(),# Retrieve all Category objects
    template_name = 'warehouses/Category_list.html', # Template to render
    context_object_name = 'warehouses'  # Context variable name       
    )
        
category_list_view = Categorylist().as_view()



def Category_detail(request,Category_id):
    try:
        warehouses = Category.objects.get(pk=Category_id) # Retrieve the Category instance by primary key
    except Category.DoesNotExist:
        return HttpResponseNotFound()  # Return a 404 response if the Category does not exist
    
    # Retrieve all items associated with the Category, ordered by quantity
    items = Item.objects.filter(Category = warehouses).order_by('quantity')

    #prepare data for chart
    labels = [item.name for item in items]
    quantities = [item.quantity for item in items]

    context = {'warehouses':warehouses,'items':items,'labels':labels,'quantities':quantities}
    return render(request,'warehouses/Category_detail.html',context=context)

def Category_create(request):
    """
    Handle the creation of a new Category object.

    This view processes both GET and POST requests:
    - For GET requests, it provides a blank form for the user to fill out.
    - For POST requests, it validates the submitted data, creates a new Category object 
      if the form is valid, and redirects the user to the warehouse list page.
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Create a new Category object in the database if the form data is valid
            Category.objects.create(**form.cleaned_data)
            return HttpResponseRedirect('/warehouses/')
    else:
        form = CategoryForm()# Create a blank form for the user to fill out
    # Render the 'Category_create.html' template and pass the form context
    return render(request,'warehouses/Category_create.html',{'form':form})

def Add_item(request,Category_id):
    """
    Handle the addition of a new item to a specific category.

    This view allows users to add an item to an existing category. 
    - It first checks if the category exists using the provided category ID.
    - For POST requests, it processes the form data, creates a new item linked to the category, 
      and redirects the user to the category's page.
    - For GET requests, it displays a blank form for the user to fill out.
    """
    try:
        #retrieve the category object based on the provided Category_id
        category = Category.objects.get(pk= Category_id)
    except Category.DoesNotExist:
         # If the category does not exist, return a 404 response
        return HttpResponseNotFound() 
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
           # Create a new item and associate it with the selected category
           Item.objects.create(Category=category,**form.cleaned_data)
           return HttpResponseRedirect(f'/warehouses/{Category_id}/')
    else:
        form = ItemForm()     

    return render(request,'warehouses/Add_item.html',{'form':form,'category':category})   

def Item_chart(request):
    """
    Render a chart displaying items and their respective quantities.

    This view retrieves all items from the database, orders them by their quantity,
    and prepares data for display in a chart. The item names and quantities are 
    passed to the template as context variables to be used in rendering the chart.

    """
    # Retrieve all items from the database, ordered by quantity in ascending order
    items = Item.objects.all().order_by('quantity')
    # Prepare the labels (item names) and data (quantities) for the chart
    labels = [item.name for item in items] 
    quantities = [item.quantity for item in items]

    context = {'labels':labels , 'quantities':quantities}
    
    return render(request,'warehouses/Item_chart.html',context=context)

def update_item(request,Category_id, Item_id):
    """
    Update an existing item within a specific category.

    This view allows users to update the details of an item belonging to a specified category.
    - It retrieves the item and category based on the provided IDs.
    - For POST requests, it validates and saves the updated data.
      If the item's quantity is below the threshold (e.g., 5), a notification is sent.
    - For GET requests, it displays the item's current data in a form for editing.

    Returns:
        HttpResponse: Renders the update item form or redirects to the category page.
    
    
    """
    # Retrieve the item belonging to the specified category or return a 404 error if not found
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
        item.delete()# Delete the item from the database
        return redirect('Category_detail', Category_id=Category_id)
    # Render the confirmation page to ensure the user wants to delete the item
    return render(request, 'warehouses/confirm_delete.html', {'item': item, 'Category_id': Category_id})

def home(request):
    #return HttpResponse('<h1> welcome to StockTracker </h1>')
    return render(request,'warehouses/home.html' )

def send_notification(item):
    """
    Send an email notification for items with low stock.

    This function generates a low stock alert email for the specified item and sends it 
    to a predefined recipient list. The email includes the item's name and current stock quantity.

    """
    # Define the email subject and message
    subject = f"Low Stock Alert: {item.name}"
    # Email body
    message = f"The stock for item '{item.name}' is below the threshold. Current quantity: {item.quantity}."
    # Sender email address
    from_email = 'django@mailtrap.club'
    # List of recipient email addresses
    recipient_list = ['test.mailtrap1234@gmail.com']  # Add the recipient email here

    send_mail(subject, message, from_email, recipient_list)

def expiry_check(request):
    # Calculate the date one month from now
    one_month_later = now().date()+timedelta(days=30)
    today = now().date()
    # Filter items with expiry date less than one month away
    expiring_items = Item.objects.filter(expiry__lte = one_month_later, expiry__gt = today).order_by('expiry')
    expired_items =Item.objects.filter(expiry__lte = now().date())
    context={'expiring_items':expiring_items,'expired_items':expired_items}
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


def bulk_edit_quantities(request):
    """
        Handle bulk editing of item quantities.

    This view allows users to update the quantities of multiple items at once using a formset.
    - For POST requests, it processes the submitted data, validates it, and saves the changes.
    - If any item's quantity falls below the threshold (e.g., 5), a notification is triggered.
    - For GET requests, it displays the formset populated with current item data.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the bulk edit formset or redirects after successful updates.
    """
    # Create a formset for Item model, editing only 'quantity'
    ItemFormSet = modelformset_factory(Item, form=ItemQuantityForm, extra =0)
    if request.method =='POST':
        formset = ItemFormSet(request.POST)
        if formset.is_valid():
          updated_items=formset.save() #save changes
          # Check if any updated item's quantity is below the threshold
          for item in updated_items:
              if item.quantity < 5:
                send_notification(item)# Send a notification for low stock
          return redirect('bulk_edit_quantities')
    else:
        formset = ItemFormSet(queryset = Item.objects.all())

    return render(request, 'warehouses/bulk_edit_quantities.html',{'formset': formset})        
