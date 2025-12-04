from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'style': 'width: 100%; padding: 0.75rem 1rem; border: 1px solid #cbd5e1; border-radius: 0.5rem; font-size: 1rem;'
        })
    )
    phone_number = forms.CharField(
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number',
            'style': 'width: 100%; padding: 0.75rem 1rem; border: 1px solid #cbd5e1; border-radius: 0.5rem; font-size: 1rem;'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone_number')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username',
                'style': 'width: 100%; padding: 0.75rem 1rem; border: 1px solid #cbd5e1; border-radius: 0.5rem; font-size: 1rem;'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password',
            'style': 'width: 100%; padding: 0.75rem 1rem; border: 1px solid #cbd5e1; border-radius: 0.5rem; font-size: 1rem;'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'style': 'width: 100%; padding: 0.75rem 1rem; border: 1px solid #cbd5e1; border-radius: 0.5rem; font-size: 1rem;'
        })
        # Remove help text that shows as literal {{ field.help_text }}
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create or update user profile with phone number
            phone_number = self.cleaned_data.get('phone_number', '')
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'phone_number': phone_number if phone_number else None}
            )
        return user

