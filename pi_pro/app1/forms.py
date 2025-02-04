from django.forms import ModelForm
from django import forms
from .models import Image

class Image_form(ModelForm):
    title=forms.CharField(
        label="タイトル",
        widget=forms.TextInput(attrs={"class":"form-control"}),
        required=True
    )
    image=forms.ImageField(
        label="イメージ図",
        widget=forms.FileInput(attrs={"class":"form-control"}),
        required=True
    )

    class Meta:
        model = Image
        fields = ['title','image']