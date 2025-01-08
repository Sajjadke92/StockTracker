from django import forms
from .models import Item
from django.core.exceptions import ValidationError
from django.utils.timezone import now


class CategoryForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea,required=False)


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'location', 'quantity', 'expiry', 'description' ]   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expiry'].widget = forms.DateInput(attrs={'type': 'date'})    

    def clean_expiry(self):
        expiry_date = self.cleaned_data['expiry']
        if expiry_date < now().date():
            raise ValidationError("The expiry date cannot be in the past.")
        return expiry_date    
    
class ItemQuantityForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['id','name','quantity']

    