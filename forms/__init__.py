from llama_cpp import Llama

llm = Llama(model_path="gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf",
            verbose=False,
            n_ctx=8192,  # explicit context size (0 can be unpredictable)
            n_threads=4,  # CPU threads for non-GPU work
            n_batch=512,  # increase batch size for better throughput
            n_gpu_layers=-1,  # -1 = offload ALL layers to GPU
)