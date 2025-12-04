from django import forms
from .models import Listing, Category

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'category', 'price', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Apple AirPods Pro (2nd Gen)'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01', 'min': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe the condition, features, and history of your item...'}),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or len(title.strip()) < 10:
            raise forms.ValidationError("Title must be at least 10 characters long")
        return title.strip()
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description or len(description.strip()) < 50:
            raise forms.ValidationError("Description must be at least 50 characters long")
        return description.strip()
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= 0:
            raise forms.ValidationError("Price must be greater than zero")
        return price
