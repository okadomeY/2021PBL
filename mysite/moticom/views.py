from django.shortcuts import render
from django.views import generic
from django.utils import timezone

from .models import Report

class TopView(generic.TemplateView):
    template_name = 'moticom/main.html'
    
class IndexView(generic.ListView):
    template_name = 'moticom/index.html'
    context_object_name = 'latest_report_list'
    
    def get_queryset(self):
        return Report.objects.filter(
            created_at__lte=timezone.now()
            ).order_by('-created_at')[:10]

class BoardView(generic.TemplateView):
    template_name = 'moticom/board.html'
    

class ReportView(generic.TemplateView):
    template_name = 'moticom/report.html'
    
class GenreView(generic.TemplateView):
    template_name = 'moticom/genre.html'
    
class CompleteView(generic.TemplateView):
    template_name = 'moticom/complete.html'
    
class ProfileView(generic.TemplateView):
    template_name = 'moticom/profile.html'
    
class ComplaintsView(generic.TemplateView):
    template_name = 'moticom/complaints.html'
    

class HelpView(generic.TemplateView):
    template_name = 'moticom/help.html'
    
    
class AdminView(generic.TemplateView):
    template_name = 'moticom/admin.html'
    
class AnalysisView(generic.TemplateView):
    template_name = 'moticom/analysis.html'
    
class UserView(generic.TemplateView):
    template_name = 'moticom/user.html'

class LayoutView(generic.TemplateView):
    template_name = 'moticom/layout.html'
    
class Genre_ManageView(generic.TemplateView):
    template_name = 'moticom/genre_manage.html'
    
class FilterView(generic.TemplateView):
    template_name = 'moticom/filter.html'
    
class SortingView(generic.TemplateView):
    template_name = 'moticom/sorting.html'
    
class LinkingView(generic.TemplateView):
    template_name = 'moticom/linking.html'