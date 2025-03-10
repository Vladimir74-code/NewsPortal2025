from django import forms
from .models import News, Author

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'type', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'categories': forms.CheckboxSelectMultiple(),  # Для ManyToMany
        }

class AuthorProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['ratingAuthor']
        widgets = {
            'ratingAuthor': forms.NumberInput(attrs={'class': 'form-control'}),
        }