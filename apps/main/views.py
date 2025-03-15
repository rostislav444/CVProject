import json
import os
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView
from weasyprint import CSS, HTML

from .models import CV
from .services import SUPPORTED_LANGUAGES, TranslationService
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["supported_languages"] = SUPPORTED_LANGUAGES
        return context


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
        email = request.POST.get("email")

        if not email:
            messages.error(request, "Email address is required.")
            return redirect("main:cv_detail", pk=pk)

        # Get the site URL for generating absolute URLs in the PDF
        site_url = f"{request.scheme}://{request.get_host()}"

        # Queue the Celery task to send the email
        send_cv_pdf_email.delay(pk, email, site_url)

        # Add a success message
        messages.success(request, f"CV will be sent to {email} shortly.")

        # Redirect back to the CV detail page
        return redirect("main:cv_detail", pk=pk)


class CVTranslateView(View):
    """Translate CV content"""

    def get(self, request, pk):
        # Get the language from the query params
        language = request.GET.get("language")

        if not language:
            messages.error(request, "Language is required.")
            return redirect("main:cv_detail", pk=pk)

        # Find the display name for the language
        language_display = next(
            (display for code, display in SUPPORTED_LANGUAGES if code == language),
            language,
        )

        # Get the CV
        cv = get_object_or_404(
            CV.objects.prefetch_related("skills__skill", "projects", "contacts"), pk=pk
        )

        # Prepare context with original CV
        context = {
            "cv": cv,
            "original_cv": cv,
            "supported_languages": SUPPORTED_LANGUAGES,
            "translated_language": language_display,
            "is_translation": True,
        }

        # Create a dictionary of translatable fields
        translatable_text = {
            "bio": cv.bio,
            "title": cv.title,
            "summary": cv.summary,
        }

        # Add project fields to translate
        for i, project in enumerate(cv.projects.all()):
            translatable_text[f"project_{i}_name"] = project.name
            translatable_text[f"project_{i}_description"] = project.description
            translatable_text[f"project_{i}_technologies"] = project.technologies

        # Convert to JSON for translation
        json_text = json.dumps(translatable_text)

        # Translate the JSON
        try:
            # Use Anthropic as default, fallback to OpenAI
            translated_json_text = TranslationService.translate(
                json_text,
                language_display,
                service=(
                    "anthropic" if os.environ.get("ANTHROPIC_API_KEY") else "openai"
                ),
            )

            # Parse the translated JSON
            try:
                translated_data = json.loads(translated_json_text)

                # Create a translation context
                translation_context = {
                    "bio": translated_data.get("bio", cv.bio),
                    "title": translated_data.get("title", cv.title),
                    "summary": translated_data.get("summary", cv.summary),
                    "projects": [],
                }

                # Add translated projects
                for i, project in enumerate(cv.projects.all()):
                    translation_context["projects"].append(
                        {
                            "name": translated_data.get(
                                f"project_{i}_name", project.name
                            ),
                            "description": translated_data.get(
                                f"project_{i}_description", project.description
                            ),
                            "technologies": translated_data.get(
                                f"project_{i}_technologies", project.technologies
                            ),
                            "start_date": project.start_date,
                            "end_date": project.end_date,
                            "url": project.url,
                        }
                    )

                context["translation"] = translation_context

            except json.JSONDecodeError:
                # If JSON parsing fails, try treating the response as plain text
                messages.warning(
                    request,
                    f"Translation format issue. Showing partially translated content.",
                )
                context["translation_text"] = translated_json_text

        except Exception as e:
            messages.error(request, f"Translation error: {str(e)}")

        # Render the translated CV
        return render(request, "main/cv_translated.html", context)
