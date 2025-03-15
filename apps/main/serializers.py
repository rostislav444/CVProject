from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from apps.main.models import CV, Contact, CVSkill, Project, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class CVSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), source="skill", write_only=True
    )

    class Meta:
        model = CVSkill
        fields = ["id", "skill", "skill_id", "level"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "type", "value"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "technologies",
            "start_date",
            "end_date",
            "url",
        ]


class CVSerializer(WritableNestedModelSerializer):
    skills = CVSkillSerializer(many=True)
    contacts = ContactSerializer(many=True)
    projects = ProjectSerializer(many=True)

    class Meta:
        model = CV
        fields = [
            "id",
            "firstname",
            "lastname",
            "bio",
            "title",
            "summary",
            "skills",
            "contacts",
            "projects",
            "created_at",
            "updated_at",
        ]
