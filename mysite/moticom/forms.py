#作成途中
from django import forms

from .models import Report, Genre

class ReportForm(forms.Form):
    report_text = forms.CharField(label="",
                           widget=forms.Textarea(attrs={'class':'form-control',
                                                        'cols':'50',
                                                        'rows':'6',
                                                        'onkeyup':'ShowLength(value)',
                                                        }),
                           max_length=300)
    
    

class CreatePost(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_text', 'user_id', 'genre_id']
        labels = {'report_text':"",
                  'user_id':"",
                  'genre_id':"",}
        widgets = {'report_text':forms.HiddenInput,
                   'user_id':forms.HiddenInput,
                   'genre_id':forms.RadioSelect(attrs={'class':'form-check-input',}),
                    }
                   

class AddGenre(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ('genre_name',)
        labels = {'genre_name':""}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields['genre_name'].widget.attrs['class'] = "form-control"



#以下seve_reportが上手く行っているため、削除の可能性あり
#    text = forms.CharField(label="", widget=forms.Textarea, max_length=300)
"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields['report_text'].widget.attrs['class'] = "form-control"
        self.fields['report_text'].widget.attrs['cols'] = "50"
        self.fields['report_text'].widget.attrs['rows'] = "6"
        self.fields['report_text'].widget.attrs['onkeyup'] = 'ShowLength(value)'
        self.fields['report_text'].widget = forms.Textarea
"""