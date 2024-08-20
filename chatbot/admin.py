from django.contrib import admin
from .models import CustomUser, Teacher, Briefing
from questions.models import Question

admin.site.register(CustomUser)
admin.site.register(Teacher)
admin.site.register(Question)
admin.site.register(Briefing)

# Register your models here.
