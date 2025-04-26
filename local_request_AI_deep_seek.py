"""
pip install llama-cpp-python[cuda]
"""
from llama_cpp import Llama

# Инициализация модели
response = Llama(
    model_path = r"D:\0_AI_Project\MODEL_DeepSeek-R1-Distill-Qwen-7B-Q2_K_L(GGUF)\DeepSeek-R1-Distill-Qwen-7B-Q2_K_L.gguf",
#    model_path = r"D:\0_AI_Project\MODEL_Qwen25-3B-Instruct(GGUF)\qwen2.5-3b-instruct-fp16-merged.gguf",
    #n_ctx=0,   # Неограниченное количество n_ctx
    n_gpu_layers=-1,
    verbose=False # false = не показывать данные отладки
)

# Генерация ответа
for chunk in response(
    prompt="Напиши самую простую програмку хелоу ворлд на джаве",
    max_tokens=10**6,
    stream=True  # Включаем потоковый режим
):
    print(chunk["choices"][0]["text"], end="", flush=True)
