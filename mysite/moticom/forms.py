#作成途中
from django import forms

from .models import Report, Genre, ControlMeasure, Comment

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

class CreativeControlMeasure(forms.ModelForm):
    class Meta:
        model = ControlMeasure
        fields = ("cm_name", "cm_contents", "genre_id")

class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment_text", "report_id",)
        widgets = {'report_id':forms.HiddenInput,}
        labels = {'comment_text':"",}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""