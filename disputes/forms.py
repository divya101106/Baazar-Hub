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
            # Only show transactions where user is involved and offer is accepted
            from django.db.models import Q
            self.fields['transaction'].queryset = Offer.objects.filter(
                status='accepted'
            ).filter(
                Q(buyer=self.user) | Q(listing__seller=self.user)
            ).select_related('listing', 'buyer', 'listing__seller')
    
    def clean_reason(self):
        reason = self.cleaned_data.get('reason', '').strip()
        if len(reason) < 20:
            raise forms.ValidationError("Please provide at least 20 characters describing the issue.")
        return reason

