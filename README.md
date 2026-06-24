# Setup
This demo has been setup to use postgreSQL as the database.
A compose.yaml file has been provided that will get the server running. 
You will need a .env file so the django server will properly connect to it.

Copying the data of example.env will suffice (though not secure).

## LLM
You will also need to download a LLM into the main directory as that is used for the field validation.
Expected model is `gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf`. I found this from here [https://huggingface.co/unsloth/gemma-4-26B-A4B-it-qat-GGUF](https://huggingface.co/unsloth/gemma-4-26B-A4B-it-qat-GGUF).

If you use a different .gguf model, simplest thing to do is just rename it to `gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf`.

The model worked with following parameters worked on my RX 9060XT 16GB.

```
n_ctx=8192,
n_threads=4,
n_batch=512,
n_gpu_layers=-1
```

The demo install llama-cpp-python with vulkan support.

## pip
First install llama-cpp-python with a specific backend support.
I used vulkan support.
`CMAKE_ARGS="-DGGML_VULKAN=on" pip install llama-cpp-python`

Use requirements.txt to pip install everything else
`pip install -r requirements.txt`

# Running the demo
 First get the posrtgreSQL server running with 
 `docker compose up -d db`

 Then get the django server running with
 `python manage.py runserver`

 Go to [http://localhost:8000/forms](http://localhost:8000/forms) to mess around with the what and reason fields. Those are the fields that the llm validate the content of.


## Option 2
`docker compose up -d`

This will also run the demo. Only downside is the llm will run on CPU. 
I can't figure out how to get llama-cpp-python install with vulkan support in a docker container.

This option lets you skip the pip part of the setup.
