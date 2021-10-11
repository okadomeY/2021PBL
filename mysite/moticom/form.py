#作成途中
from django import forms

class ReportForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)