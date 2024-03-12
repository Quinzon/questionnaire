from django.contrib import admin
from django.db import models
from jsoneditor.forms import JSONEditor
from .models import Form, Application


@admin.register(Form)
class JsonFieldAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditor},
    }


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'form', 'email', 'status')
