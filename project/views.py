from django.views.generic import TemplateView


class SettingsView(TemplateView):
    template_name = "settings/settings.html"