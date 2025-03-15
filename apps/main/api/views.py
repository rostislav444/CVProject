from rest_framework import viewsets
from apps.main.models import CV, Skill
from apps.main.serializers import CVSerializer, SkillSerializer


class CVViewSet(viewsets.ModelViewSet):
    queryset = CV.objects.all().prefetch_related('skills', 'contacts', 'projects')
    serializer_class = CVSerializer


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer