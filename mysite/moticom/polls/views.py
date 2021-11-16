from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:5]
    
    
    """未来の投稿が公開されないように変更する前
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]
    """    
        
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    #公開日前投稿除外処理追加
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    
    
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=
        (question.id,)))
    

""""汎用ビュー変換前
#from django.http import Http404
#from django.shortcuts import render
#from django.http import HttpResponse
#from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Choice, Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list}
#    return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
#get_object_or_404の私用で不要に
#    try:
#        question = Question.objects.get(pk=question_id)
#    except Question.DoesNotExist:
#        raise Http404("Question does not exist")
#render()の私用で不要に
#    return HttpResponse("You're looking at question %s." % question_id)
    return render(request, "polls/detail.html", {'question': question})   

def results(request, question_id):
#render()の私用で不要に
#    response = "You're looking at the results of question %s."
#    return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {'question': question})

def vote(request, question_id):
#index.htmlにフォームを書いた後
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=
        (question.id,)))
        
#フォーム追記前    
#render()の私用で不要に
#    return HttpResponse("You're voting on question %s." % question_id)
#    return render(request, "You're voting on question %s." % question_id)
"""