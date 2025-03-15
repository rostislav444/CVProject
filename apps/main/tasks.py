from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO
from apps.main.models import CV


@shared_task
def send_cv_pdf_email(cv_id, recipient_email, site_url):
    """
    Task to generate PDF from CV and email it
    """
    try:
        # Get the CV
        cv = CV.objects.prefetch_related('skills__skill', 'projects', 'contacts').get(pk=cv_id)
        
        # Render the PDF template with context
        html_string = render_to_string('main/cv_pdf.html', {'cv': cv})
        
        # Create a PDF file
        pdf_file = BytesIO()
        HTML(string=html_string, base_url=site_url).write_pdf(pdf_file)
        pdf_file.seek(0)
        
        # Create email message
        subject = f"CV of {cv.full_name}"
        message = f"Please find attached the CV of {cv.full_name}."
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email],
        )
        
        # Attach the PDF
        email.attach(f"{cv.firstname}_{cv.lastname}_CV.pdf", pdf_file.read(), 'application/pdf')
        
        # Send email
        email.send()
        
        return {"status": "success", "message": f"CV sent to {recipient_email}"}
    except CV.DoesNotExist:
        return {"status": "error", "message": "CV not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}