from django import forms

class CategoryForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea,required=False)


class ItemForm(forms.Form):
    name = forms.CharField()
    location = forms.CharField()
    quantity = forms.IntegerField()
    expiry = forms.DateField()
    description = forms.CharField(required=False)