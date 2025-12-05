from django import forms
from .models import Dispute
from offers.models import Offer

class DisputeForm(forms.ModelForm):
    """Form for submitting a dispute"""
    transaction = forms.ModelChoiceField(
        queryset=Offer.objects.none(),  # Will be filtered in view
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'width: 100%; padding: 0.75rem 1rem; border: 1px solid #cbd5e1; border-radius: 0.5rem; font-size: 1rem;'
        })
    )
    reason = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Please describe the issue with this transaction...',
            'style': 'width: 100%; padding: 0.75rem 1rem; border: 1px solid #cbd5e1; border-radius: 0.5rem; font-size: 1rem;'
        }),
        min_length=20,
        help_text='Please provide at least 20 characters describing the issue.'
    )
    
    class Meta:
        model = Dispute
        fields = ['transaction', 'reason']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            # Only show the latest purchased item (most recent completed payment)
            from django.db.models import Q
            from payments.models import Payment
            # Get the most recent completed payment for this user as buyer
            latest_payment = Payment.objects.filter(
                buyer=self.user,
                status='completed'
            ).select_related('offer', 'offer__listing').order_by('-completed_at').first()
            
            if latest_payment:
                # Show only the latest purchased item
                self.fields['transaction'].queryset = Offer.objects.filter(
                    id=latest_payment.offer.id
                ).select_related('listing', 'buyer', 'listing__seller')
            else:
                # No completed payments, show empty queryset
                self.fields['transaction'].queryset = Offer.objects.none()
    
    def clean_reason(self):
        reason = self.cleaned_data.get('reason', '').strip()
        if len(reason) < 20:
            raise forms.ValidationError("Please provide at least 20 characters describing the issue.")
        return reason

