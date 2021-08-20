from django.contrib import admin

from .models import Choice, Question

#ChoiceオブジェクトをQuestionと同時に使出来るようにする
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

#adminフォームのカスタマイズで追加2
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ]
    inlines = [ChoiceInline]
        
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    
    """ChoiceオブジェクトをQuestionと同時に使出来るようにするため変更
    ('Date information', {'fields': ['pub_date']}),
    ]
    """
"""
#adminフォームのカスタマイズで追加1
    公開日と質問文の表示順を入れ替える
class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']
"""

"""簡単なchoice追加方法（不便なため別な方法に変更）
admin.site.register(Choice)
"""

admin.site.register(Question, QuestionAdmin)



