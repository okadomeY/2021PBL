#作成途中
from django import forms
from django.core.validators import ValidationError
from django.contrib.auth import get_user_model

from .models import Report, Genre, ControlMeasure, Comment, NGWord

#NGワード処理（要修正→NGワードをDBから取得、NGワード判定）
def ng_word(value):
    NG_WORDS=NGWord.objects.all().values_list('ng_words', flat=True)#←DBから取得するように修正が必要
    print(NG_WORDS)
    for ng in NG_WORDS:
        if value.find(ng) != -1:
            raise ValidationError('禁止用語が含まれています。')

class ReportForm(forms.Form):
    report_text = forms.CharField(label="",
                                  widget=forms.Textarea(attrs={'class':'form-control',
                                                        'cols':'50',
                                                        'rows':'6',
                                                        'onkeyup':'ShowLength(value)',
                                                        }),
                                  max_length=300,
                                  validators=[ng_word],
                                 )
    

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

class UserCreationForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = get_user_model()
        fields = ('email',)
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class AddNgWord(forms.ModelForm):
    class Meta:
        model = NGWord
        fields = ('ng_words',)
        labels = {'ng_words':"",}
        