import os
import json
import time
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the original CAPTCHA solving function
from capt_recog_with_AI import send_request_to_ai


def read_models_list(file_path):
    """Read models from the text file"""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def read_existing_working_models(file_path):
    """Read existing working models from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_working_models(file_path, model, response_time, captcha_code, expected_number):
    """Update working models JSON file"""
    # Read existing models
    working_models = read_existing_working_models(file_path)

    # Add new model with detailed information
    working_models[model] = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "response_time_ms": response_time,
        "captcha_result": captcha_code,
        "expected_number": expected_number,
        "solved_correctly": captcha_code == str(expected_number)
    }

    # Write updated models back to file
    with open(file_path, 'w') as f:
        json.dump(working_models, f, indent=4)


def test_models(models_file, working_models_file, image_path, expected_number, api_key, base_url):
    """Test all models for CAPTCHA solving (single request per model)"""
    # Read list of models
    models = read_models_list(models_file)

    # Iterate through models
    for model in models:
        print(f"\nTesting model: {model}")

        # Measure response time
        start_time = time.time()

        # Attempt to solve CAPTCHA
        try:
            captcha_code = send_request_to_ai(
                image_path,
                api_key,
                base_url,
                model
            )

            # Calculate response time
            response_time = int((time.time() - start_time) * 1000)

            # Check if model correctly solved the CAPTCHA
            if captcha_code == str(expected_number):
                print(f"Model {model} SUCCESSFULLY solved CAPTCHA!")
                print(f"Response Time: {response_time} ms")
                print(f"CAPTCHA Result: {captcha_code}")
            else:
                print(f"Model {model} FAILED to solve CAPTCHA. Got: {captcha_code}")

            # Update working models file with single request result
            update_working_models(
                working_models_file,
                model,
                response_time,
                captcha_code,
                expected_number
            )

        except Exception as e:
            print(f"Error testing model {model}: {e}")

            # Update working models file with error information
            update_working_models(
                working_models_file,
                model,
                None,
                "ERROR",
                expected_number
            )


def main():
    # Configuration from original script
    API_KEY = "sk-or-v1-..."
    BASE_URL = "https://openrouter.ai/api/v1"

    # Paths and expected number
    models_file = 'free_AI_models_all.txt'
    working_models_file = 'free_AI_models_working.json'
    image_path = 'captcha_screenshots/captcha_20250408_005533.png'
    expected_number = 590

    # Run model testing
    test_models(
        models_file,
        working_models_file,
        image_path,
        expected_number,
        API_KEY,
        BASE_URL
    )


if __name__ == "__main__":
    main()