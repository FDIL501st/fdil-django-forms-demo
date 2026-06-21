from logging import log

from django.forms import ModelForm
from .models import Report
from . import llm

SYSTEM_PROMPT = """
You will be asked yes or no questions. You will only answer with a 'yes' or a 'no'.
"""

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

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT }
        ]
        what_prompt = f"Is the following describing an event: {what}"
        reason_prompt = f"If you answered no previously, answer no again. Is the following a reason for sharing the previously mentioned event: {reson}"

        messages.append({"role": "user", "content": what_prompt })
        response1 = llm.create_chat_completion(messages = messages, temperature=1.0, top_p=0.95, top_k=64)
        response1_msg = response1["choices"][0]["message"]["content"] # type: ignore
        log(level=5, msg=response1_msg)

        messages.append(response1["choices"][0]["message"])
        messages.append({"role": "user", "content": reason_prompt })
        response2 = llm.create_chat_completion(messages=messages, temperature=1.0, top_p=0.95, top_k=64)
        response2_msg = response2["choices"][0]["message"]["content"]
        log(level=5, msg=response2_msg)
        messages.append(response2["choices"][0]["message"])


        if response1_msg.lower() != "yes":
            self.add_error("what", "Does not explain what happens.")

        if response2_msg.lower() != "yes":
            self.add_error("reason", "Does not explain why the report was made.")


        print(messages)

        return cleaned