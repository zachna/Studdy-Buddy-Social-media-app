from cProfile import Profile
from django.contrib import admin
from .models import Profile,StudySessionModel, Class
# Register your models here.
admin.site.register(Profile)
admin.site.register(StudySessionModel)

class ClassAdmin(admin.ModelAdmin):
    list_display = ('course_number_field', 'subject_field', 'catalog_number_field', 'instructor_field')
admin.site.register(Class, ClassAdmin)