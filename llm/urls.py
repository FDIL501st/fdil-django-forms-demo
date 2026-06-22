from django.urls import path

from . import views

app_name = "llm"

urlpatterns = [
    path("validate_form_fields/", views.validate_form_fields, name="validate_form_fields"),
]