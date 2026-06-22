from logging import log

from django.forms import ModelForm
from .models import Report
from requests import request
from django.urls import reverse

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ["name", "date", "what", "where", "reason"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # tailwind styling
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "border-2 border-black"})

    def clean(self):
        cleaned = super().clean()
        if not cleaned:
            # not expecting cleaned to be None, so not sure how to deal with this
            # raise an exception?
            return cleaned

        what = cleaned.get("what")
        reson = cleaned.get("reason")
        # url = "http://localhost:8000/"+reverse('llm:validate_form_fields')
        res = request('POST', url="http://localhost:8000/"+reverse('llm:validate_form_fields'),json={'what': what, 'reason': reson})
        # need to figure out how to make this POST call less hardcoded
        # is there a way to programmatically create the host with function calls?
        res_json = res.json()
        response1_msg = res_json.get("what_answer")
        response2_msg = res_json.get("reason_answer")

        # Better programming would be checking if response1 and response2 were None
        # should not be but possible if start changing codebase and change return names

        if response1_msg.lower() != "yes":
            self.add_error("what", "Does not explain what happens.")

        if response2_msg.lower() != "yes":
            self.add_error("reason", "Does not explain why the report was made.")

        return cleaned