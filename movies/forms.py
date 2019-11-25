from .models import Review, Score
from django import forms

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('user','movie')
class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        exclude = ('user','movie')