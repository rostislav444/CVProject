from django.views.generic import ListView, DetailView

from .models import CV


class CVListView(ListView):
    model = CV
    template_name = 'main/cv_list.html'
    context_object_name = 'cvs'
    
    def get_queryset(self):
        return CV.objects.all().prefetch_related(
            'skills__skill',  # Получаем навыки и их названия
            'contacts',       # Получаем контакты
            'projects'        # Получаем проекты
        )


class CVDetailView(DetailView):
    model = CV
    template_name = 'main/cv_detail.html'
    context_object_name = 'cv'
    
    def get_queryset(self):
        return CV.objects.prefetch_related('skills', 'projects', 'contacts')
