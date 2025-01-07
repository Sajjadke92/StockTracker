"""
URL configuration for StockTracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path



from warehouses.views import home,Category_detail,Category_create,category_list_view,Add_item,Item_chart,delete_item,update_item,expiry_check, search, item_detail


urlpatterns = [
    path("admin/", admin.site.urls),
    path("",home),
    path('warehouses/create/',Category_create, name='Category_create'),
    path('warehouses/',category_list_view,name='Category_list'),
    path('warehouses/<int:Category_id>/',Category_detail,name='Category_detail'),
    path('warehouses/<int:Category_id>/Add_Item/',Add_item,name='Add_Item'),
    path('warehouses/Item_chart/',Item_chart,name='item_chart'),
    path('warehouses/<int:Category_id>/delete_item/<int:Item_id>/',delete_item, name='delete_item'),
    path('warehouses/<int:Category_id>/update_item/<int:Item_id>/',update_item,name='update_item'),
    path('warehouses/expiry_check/',expiry_check,name='expiry_check'),
    path('warehouses/search/',search, name='search'),
    path('warehouses/search/<int:item_id>/',item_detail, name='item_detail'),
]
