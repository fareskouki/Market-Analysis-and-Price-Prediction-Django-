from django import forms
from .models import News,NewsArticle,Comment  
from django.db import models 

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'description', 'pdf_file']

class UploadFileForm(forms.Form):
    file = forms.FileField()

class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['title', 'content']
        labels = {
            'title': 'Article Title',
            'content': 'Article Content',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }


class PDFUploadForm(forms.ModelForm):
    pdf_file = forms.FileField(required=True, help_text="Upload a PDF with news content.")

    class Meta:
        model = NewsArticle
        fields = ['pdf_file']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  