from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from llama_cpp import Llama


# Create your views here.



llm = Llama(model_path="gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf",
            verbose=False,
            n_ctx=8192,  # explicit context size (0 can be unpredictable)
            n_threads=4,  # CPU threads for non-GPU work
            n_batch=512,  # increase batch size for better throughput
            n_gpu_layers=-1,  # -1 = offload ALL layers to GPU
)

SYSTEM_PROMPT = """
You will be asked yes or no questions. You will only answer with a 'yes' or a 'no'.
"""

@api_view(['POST'])
@parser_classes([JSONParser])
def validate_form_fields(request):
    """The form fields that should be validated. Expecting the what field and reason field."""
    data = request.data

    # expecting data.what and data.reason

    if data is None:
        return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

    what = data.get('what', None)
    reason = data.get('reason', None)
    if what is None:
        return Response({"error": "Missing what value"}, status=status.HTTP_400_BAD_REQUEST)
    if reason is None:
        return Response({"error": "Missing reason value"}, status=status.HTTP_400_BAD_REQUEST)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    what_prompt = f"Is the following describing an event: {what}"
    reason_prompt = f"If you answered no previously, answer no again. Is the following a reason for sharing the previously mentioned event: {reason}"

    messages.append({"role": "user", "content": what_prompt})
    response1 = llm.create_chat_completion(messages=messages, temperature=1.0, top_p=0.95, top_k=64) # type: ignore

    messages.append(response1["choices"][0]["message"]) # type: ignore
    what_answer = messages[-1]["content"]
    messages.append({"role": "user", "content": reason_prompt})
    response2 = llm.create_chat_completion(messages=messages, temperature=1.0, top_p=0.95, top_k=64) # type: ignore
    messages.append(response2["choices"][0]["message"]) # type: ignore
    reason_answer = messages[-1]["content"]

    response = {
        "what_answer": what_answer,
        "reason_answer": reason_answer,
    }
    print(response)
    return Response(response, status=status.HTTP_200_OK)


