from django.contrib import admin
from .models import Choice, Question # Bring in the database schema

# Register your models here.
admin.site.register(Choice)
admin.site.register(Question)
