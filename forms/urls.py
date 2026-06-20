from django.urls import path

from . import views

app_name = "forms"

urlpatterns = [
    path("", views.report, name="report"),
    path("<int:pk>/", views.ReportView.as_view(), name="view_report"),
]