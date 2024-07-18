from django.contrib import admin
from .models import CustomUser, Teacher
from questions.models import Question

admin.site.register(CustomUser)
admin.site.register(Teacher)
admin.site.register(Question)

# Register your models here.
