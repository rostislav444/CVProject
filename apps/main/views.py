import os
import json
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView
from weasyprint import CSS, HTML

from .models import CV
from .tasks import send_cv_pdf_email


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


class CVEmailPDFView(View):
    """Send CV as PDF via email using Celery"""
    
    def post(self, request, pk):
        # Get the email from the form
        email = request.POST.get('email')
        
        if not email:
            messages.error(request, "Email address is required.")
            return redirect('main:cv_detail', pk=pk)
            
        # Get the site URL for generating absolute URLs in the PDF
        site_url = f"{request.scheme}://{request.get_host()}"
        
        # Queue the Celery task to send the email
        send_cv_pdf_email.delay(pk, email, site_url)
        
        # Add a success message
        messages.success(request, f"CV will be sent to {email} shortly.")
        
        # Redirect back to the CV detail page
        return redirect('main:cv_detail', pk=pk)
