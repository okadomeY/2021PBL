from django.shortcuts import render
from django.views import generic
from django.utils import timezone

from .models import Report

class TopView(generic.ListView):
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
    

class ComplaintsView(generic.TemplateView):
    template_name = 'moticom/complaints.html'
    

class HelpView(generic.TemplateView):
    template_name = 'moticom/help.html'
    
    
class AdminView(generic.TemplateView):
    template_name = 'moticom/admin.html'