import os
import re
import time
import importlib.util
import sys
from datetime import datetime
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def import_module_from_path(module_path):
    """
    Dynamically import a module from a specific file path

    Args:
        module_path (str): Path to the Python module

    Returns:
        module: Imported module
    """
    module_name = os.path.splitext(os.path.basename(module_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def capture_captcha_screenshot(driver, max_attempts=1):
    """
    Capture precise screenshot of captcha element with AI-based CAPTCHA recognition

    Args:
        driver: Selenium WebDriver instance
        max_attempts (int): Maximum number of recognition attempts

    Returns:
        bool: True if captcha solved successfully, False otherwise
    """
    for attempt in range(max_attempts):
        try:
            # Check if captcha image is present
            captcha_img = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'show_reg_img/security_battle.php')]"))
            )

            if captcha_img and captcha_img.is_displayed():
                print(f"Captcha detected! Attempting to solve... (Attempt {attempt + 1})")

                # Find the captcha input field
                captcha_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@name='code21']"))
                )

                # Create screenshots directory if it doesn't exist
                os.makedirs('captcha_screenshots', exist_ok=True)

                # Generate unique filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = os.path.join('captcha_screenshots', f'captcha_{timestamp}.png')

                # Take screenshot of just the captcha element
                captcha_img.screenshot(screenshot_path)

                # Ensure absolute path is used
                absolute_screenshot_path = os.path.abspath(screenshot_path)
                print(f"Captcha screenshot saved at: {absolute_screenshot_path}")

                # Import the AI CAPTCHA recognition module
                try:
                    capt_recog_module = import_module_from_path('capt_recog_with_AI.py')
                except Exception as e:
                    print(f"Error importing AI CAPTCHA recognition module: {e}")
                    return False

                # Use AI to solve the CAPTCHA
                captcha_text = capt_recog_module.main(absolute_screenshot_path)

                # Validate captcha text (ensure it's a 3-digit number)
                if captcha_text and re.match(r'^\d{3}$', captcha_text):
                    # Enter the captcha text
                    captcha_input.clear()
                    captcha_input.send_keys(captcha_text)

                    print(f"Entered captcha text: {captcha_text}")
                    time.sleep(0.5)

                    return True
                else:
                    print(f"Invalid captcha text detected: {captcha_text}")
                    continue  # Try again

        except Exception as e:
            print(f"Error handling captcha (Attempt {attempt + 1}): {e}")

    print("Failed to solve CAPTCHA after maximum attempts")
    return False

def solve_captcha(driver):
    """
    Wrapper function for captcha solving

    Args:
        driver: Selenium WebDriver instance

    Returns:
        bool: True if captcha was handled successfully or wasn't present
    """
    try:
        return capture_captcha_screenshot(driver)
    except Exception as e:
        print(f"Unexpected error in solve_captcha: {e}")
        return False