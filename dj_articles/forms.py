from django import forms

from .models import Article


class ArticleCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'image', 'text', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'category': forms.Select(attrs={'class': 'form-select mb-2'}),
            'image': forms.FileInput(attrs={'class': 'form-control mb-2'}),
            'text': forms.Textarea(attrs={'class': 'form-control mb-2', 'rows': 4}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control mb-2'})
        }
