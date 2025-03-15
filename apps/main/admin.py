from django.contrib import admin
from apps.main.models import CV, Skill, CVSkill, Contact, Project


class CVSkillInline(admin.TabularInline):
    model = CVSkill
    extra = 1


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1


class ProjectInline(admin.StackedInline):
    model = Project
    extra = 1


@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('firstname', 'lastname', 'title', 'summary', 'bio')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ContactInline, CVSkillInline, ProjectInline]
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('firstname', 'lastname', 'title')
        }),
        ('Details', {
            'fields': ('summary', 'bio')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'cv_count')
    search_fields = ('name',)
    
    def cv_count(self, obj):
        return obj.cvs.count()
    cv_count.short_description = 'Number of CVs'


@admin.register(CVSkill)
class CVSkillAdmin(admin.ModelAdmin):
    list_display = ('cv', 'skill', 'level')
    list_filter = ('level', 'skill')
    search_fields = ('cv__firstname', 'cv__lastname', 'skill__name')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('cv', 'type', 'value')
    list_filter = ('type',)
    search_fields = ('cv__firstname', 'cv__lastname', 'value')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'cv', 'start_date', 'end_date', 'has_url')
    list_filter = ('start_date', 'end_date')
    search_fields = ('name', 'description', 'technologies', 'cv__firstname', 'cv__lastname')
    
    def has_url(self, obj):
        return bool(obj.url)
    has_url.boolean = True
    has_url.short_description = 'Has URL'
