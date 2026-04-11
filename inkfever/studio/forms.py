from django import forms
from .models import Booking, Review


# 🔥 BOOKING FORM (used in final step)
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['description']   # slot, artist, user handled in view

        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your tattoo idea...',
                'rows': 4
            }),
        }


# ⭐ REVIEW FORM (clean version)
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['artist', 'rating', 'comment']

        widgets = {
            'artist': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }