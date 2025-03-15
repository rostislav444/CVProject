from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class CV(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    bio = models.TextField()
    title = models.CharField(max_length=200, help_text="Professional title or role")
    summary = models.TextField(help_text="Brief professional summary")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "CV"
        verbose_name_plural = "CVs"
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}'s CV"
    
    @property
    def full_name(self):
        return f"{self.firstname} {self.lastname}"
    

class CVSkill(models.Model):
    class SkillLevel:
        BEGINNER = 'beginner'
        INTERMEDIATE = 'intermediate'
        ADVANCED = 'advanced'
        EXPERT = 'expert'

        CHOICES = [
            (BEGINNER, 'Beginner'),
            (INTERMEDIATE, 'Intermediate'),
            (ADVANCED, 'Advanced'),
            (EXPERT, 'Expert'),
        ]

    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='cvs')
    level = models.CharField(max_length=50, choices=SkillLevel.CHOICES)
    
    

class Contact(models.Model):
    class ContactType:
        EMAIL = 'email'
        PHONE = 'phone'
        LINKEDIN = 'linkedin'
        GITHUB = 'github'
        WEBSITE = 'website'

        CHOICES = [
            (EMAIL, 'Email'),
            (PHONE, 'Phone'),
            (LINKEDIN, 'LinkedIn'),
            (GITHUB, 'GitHub'),
            (WEBSITE, 'Website'),
        ]

    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='contacts')
    type = models.CharField(max_length=50, choices=ContactType.CHOICES)
    value = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.get_type_display()}: {self.value}"


class Project(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.name


