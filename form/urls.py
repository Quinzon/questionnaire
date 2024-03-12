from django.urls import path
from .views import form, questions
from django.views.generic import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='form/index.html')),
    path('<str:form_name>/', form, name='form'),
    path('<str:form_name>/questions', questions, name='questions'),
]
