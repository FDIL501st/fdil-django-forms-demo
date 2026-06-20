from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from .forms import ReportForm
from .models import Report


# Create your views here.

class ReportView(generic.DetailView):
    model = Report
    template_name = "forms/view_report.html"
    context_object_name = "report"

@require_http_methods(["GET", "POST"])
def report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report_data = form.save(commit=False)   # don't save to database
            # form validation here?
            report_data.save()  # actually save to database
            return HttpResponseRedirect(reverse("forms:view_report", args=(report_data.id,)))
        else:
            # render page with errors and form untouched
            return render(request, "forms/report.html", {"form": form,})
    else:
        # GET request, need to display form
        form = ReportForm()
        return render(request, "forms/report.html", {"form": form})

