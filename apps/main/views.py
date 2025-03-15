import os
from io import BytesIO

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import DetailView, ListView
from weasyprint import CSS, HTML

from .models import CV


class CVListView(ListView):
    model = CV
    template_name = "main/cv_list.html"
    context_object_name = "cvs"

    def get_queryset(self):
        return CV.objects.all().prefetch_related(
            "skills__skill",  # Получаем навыки и их названия
            "contacts",  # Получаем контакты
            "projects",  # Получаем проекты
        )


class CVDetailView(DetailView):
    model = CV
    template_name = "main/cv_detail.html"
    context_object_name = "cv"

    def get_queryset(self):
        return CV.objects.prefetch_related("skills", "projects", "contacts")


class CVPDFView(View):
    """Generate PDF version of a CV"""

    def get(self, request, pk):
        # Get the CV
        cv = get_object_or_404(
            CV.objects.prefetch_related("skills__skill", "projects", "contacts"), pk=pk
        )

        # Render the CV template with context
        html_string = render_to_string(
            "main/cv_pdf.html", {"cv": cv, "request": request}
        )

        # Create a PDF file
        pdf_file = BytesIO()
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
            pdf_file,
            stylesheets=[
                # Add your CSS files here if needed
                # CSS(os.path.join(settings.BASE_DIR, 'static/css/style.css')),
            ],
        )

        # Create HTTP response with PDF
        pdf_file.seek(0)
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="{cv.firstname}_{cv.lastname}_CV.pdf"'
        )

        return response
