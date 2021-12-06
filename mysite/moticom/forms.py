#作成途中
from django import forms
from django.core.validators import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm#, PasswordChangeForm
from django.contrib.auth.models import User

from .models import Report, Genre, ControlMeasure, Comment, NGWord, Account

#NGワード処理（要修正→NGワードをDBから取得、NGワード判定）
def ng_word(value):
    NG_WORDS=NGWord.objects.all().values_list('ng_words', flat=True)#←DBから取得するように修正が必要
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
        fields = ['report_text', 'user_id', 'genre_id', 'cm_id']
        labels = {'report_text':"",
                  'user_id':"",
                  'genre_id':"",
                  'cm_id':"",
                  }
        widgets = {'report_text':forms.HiddenInput,
                   'user_id':forms.HiddenInput,
                   'genre_id':forms.RadioSelect(attrs={'class':'form-check-input',}),
                   'cm_id':forms.HiddenInput,
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
        widgets = {'cm_contents':forms.Textarea,
                   }


        
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
        

class SearchForm(forms.Form):
    freeword = forms.CharField(min_length=1, max_length=20, label='', required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

#class LoginForm(AuthenticationForm):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        
#        for field in self.fields.values():
#            field.widget.attrs['class'] = 'form-control'

        
#class SignUpForm(UserCreationForm):
#
#    class Meta:
#        model = User
#        if User.USERNAME_FIELD == 'email':
#            fields = ('email',)
#        else:
#            fields = ('username', 'email')
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        for field in self.fields.values():
#            field.widget.attrs['class'] = 'form-control'

#class AccountForm(forms.ModelForm):
    # パスワード入力：非表示対応
#    password = forms.CharField(widget=forms.PasswordInput(),label="パスワード")

#    class Meta():
        # ユーザー認証
#        model = User
        # フィールド指定
#        fields = ('username','email','password')
        # フィールド名指定
#        labels = {'username':"ユーザーID",'email':"メール"}

#class AddAccountForm(forms.ModelForm):
#    class Meta():
#        # モデルクラスを指定
#        model = Account
#        fields = ('user_name',)
#        labels = {'user_name':"名前",}


#class MyPasswordChangeForm(PasswordChangeForm):
#    """パスワード変更フォーム"""

#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        for field in self.fields.values():
#            field.widget.attrs['class'] = 'form-control'
