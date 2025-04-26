import os
import re
import base64
from openai import OpenAI


def send_request_to_ai(image_path, api_key, base_url, model, max_attempts=3):
    """
    Solve CAPTCHA using AI by sending the image and requesting 3-digit code

    Args:
        image_path (str): Path to the CAPTCHA image
        api_key (str): OpenRouter API key
        base_url (str): OpenRouter base URL
        model (str): AI model to use for CAPTCHA solving
        max_attempts (int): Maximum number of attempts to solve CAPTCHA

    Returns:
        str: Extracted 3-digit CAPTCHA code or None if extraction fails
    """
    for attempt in range(max_attempts):
        try:
            # Initialize OpenAI client with OpenRouter configuration
            client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )

            # Open the image and convert to base64
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

            # Create the prompt for AI
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please analyze this CAPTCHA image and return ONLY the 3-digit number shown. Do not include any additional text or explanation. If you cannot see the number clearly, say 'UNCLEAR'."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]

            # Send request to AI
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )

            # Extract and validate the response
            ai_response = response.choices[0].message.content.strip()
            print(f"AI Response (Attempt {attempt + 1}): {ai_response}")

            # Validate that response is exactly 3 digits
            if re.match(r'^\d{3}$', ai_response):
                print(f"AI extracted CAPTCHA: {ai_response}")
                return ai_response
            elif ai_response == 'UNCLEAR':
                print("AI could not clearly read the CAPTCHA. Retrying...")
            else:
                print(f"Invalid AI response: {ai_response}")

        except Exception as e:
            print(f"Error solving CAPTCHA with AI (Attempt {attempt + 1}): {e}")

    print("Failed to solve CAPTCHA after maximum attempts")
    return None


def main(image_path):
    # Configuration

    MODEL = "qwen/qwen2.5-vl-3b-instruct:free"
    API_KEY = "sk-or-v1-..."
    BASE_URL = "https://openrouter.ai/api/v1"

    # Check if the image exists
    if not os.path.exists(image_path):
        print(f"Image {image_path} does not exist!")
        return None

    # Solve the CAPTCHA
    captcha_code = send_request_to_ai(image_path, API_KEY, BASE_URL, MODEL)

    if captcha_code:
        print(f"Final CAPTCHA Code: {captcha_code}")
        return captcha_code
    else:
        print("Failed to solve CAPTCHA")
        return None


if __name__ == "__main__":
    main('captcha_screenshots/captcha_20250326_151837.png')
    expected_number_of_picture = 991