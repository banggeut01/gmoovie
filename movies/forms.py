from django import forms
from .models import Review, Wish

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('user','movie')

# class WishForm(forms.ModelForm):
#     class Meta:
#         model = Wish
#         exclude = ('movie', 'user', 'is_male')