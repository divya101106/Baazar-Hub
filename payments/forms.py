from django import forms
from .models import Payment

class PaymentForm(forms.Form):
    """Form for payment with UPI PIN"""
    upi_id = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter UPI ID (e.g., pay@paytm)',
            'style': 'width: 100%; padding: 0.75rem 1rem; border: 1px solid #cbd5e1; border-radius: 0.5rem; font-size: 1rem;'
        })
    )
    upi_pin = forms.CharField(
        max_length=6,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter UPI PIN',
            'style': 'width: 100%; padding: 0.75rem 1rem; border: 1px solid #cbd5e1; border-radius: 0.5rem; font-size: 1rem;',
            'maxlength': '6'
        }),
        help_text='Use: pay@paytm with PIN: 1234'
    )
    
    def clean_upi_id(self):
        upi_id = self.cleaned_data.get('upi_id', '').strip().lower()
        return upi_id
    
    def clean_upi_pin(self):
        upi_pin = self.cleaned_data.get('upi_pin', '').strip()
        return upi_pin

