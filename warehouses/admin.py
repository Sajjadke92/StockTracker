from django.contrib import admin

from .models import Category,Item



class ItemAdminInline(admin.TabularInline):
    model = Item 
    fields = ['id','name','quantity','location','expiry']
    extra = 0

@admin.register(Category)    
class CaregoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines=[ItemAdminInline,] 






