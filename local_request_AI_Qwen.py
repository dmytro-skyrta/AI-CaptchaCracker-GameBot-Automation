from llama_cpp import Llama
from PIL import Image
import pytesseract
import os

def recognize_numbers_from_image(image_path):
    # Загрузка локальной модели Qwen2.5
    model = Llama(
#        model_path = r"D:\0_AI_Project\MODEL_Qwen25-3B-Instruct(GGUF)\qwen2.5-3b-instruct-fp16-merged.gguf",
        model_path = r"D:\0_AI_Project\MODEL_DeepSeek-R1-Distill-Qwen-7B-Q2_K_L(GGUF)\DeepSeek-R1-Distill-Qwen-7B-Q2_K_L.gguf",
        n_ctx = 2048,    # Контекстное окно
        n_gpu_layers=-1  # Использование GPU, если доступно
    )

    # Открытие и обработка изображения с помощью Tesseract OCR
    image = Image.open(image_path)

    # Распознавание текста/цифр
    numbers_text = pytesseract.image_to_string(image, config='--psm 6 -c tessedit_char_whitelist=0123456789')

    # Очистка результата
    numbers = [char for char in numbers_text if char.isdigit()]

    # Формирование промпта для модели
    prompt = f"""
    На изображении находятся ровно три цифры, перечёркнутые двумя лигиями.
    Пожалуйста, распознай эти три цифры и скажи, какие именно три цифры ты видишь. 
    Дай ответ в виде трезначного числа и не в ключай в него никаких другие символы, слова или обьяснения.
    """

    # Генерация ответа с помощью модели
    output = model(
        prompt,
        max_tokens=200,
        stop=["</response>"],
        echo=False
    )

    # Извлечение текста ответа
    model_response = output['choices'][0]['text'].strip()

    return {
        'tesseract_numbers': numbers,
        'model_verification': model_response
    }


# Путь к изображению
image_path = 'captcha_screenshots/captcha_20250326_151721.png'

# Распознавание цифр
result = recognize_numbers_from_image(image_path)

# Вывод результатов
print("Цифры, распознанные Tesseract:", result['tesseract_numbers'])
print("Верификация модели Qwen2.5:", result['model_verification'])