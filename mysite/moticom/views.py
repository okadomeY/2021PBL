from django.shortcuts import render
from django.views import generic

class TopView(generic.TemplateView):
    template_name = 'moticom/index.html'


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