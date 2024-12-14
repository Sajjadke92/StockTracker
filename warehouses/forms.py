from django import forms

class CategoryForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea,required=False)
