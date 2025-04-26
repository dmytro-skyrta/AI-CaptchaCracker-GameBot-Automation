from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import random

class Bot:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.driver = None

    def initialize_driver(self):
        """Initialize the webdriver with appropriate options"""
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-application-cache')
        options.add_argument('--disable-infobars')

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(60)
        self.driver.implicitly_wait(10)

    def login_to_game(self):
        """Log in to the game website"""
        print("Logging in to the game...")
        try:
            self.driver.get("https://.........../")

            # Enter login credentials
            login_field = self.driver.find_element(By.NAME, "login")
            password_field = self.driver.find_element(By.NAME, "psw")
            login_button = self.driver.find_element(By.XPATH, "//input[@value='Войти']")

            login_field.send_keys(self.login)
            password_field.send_keys(self.password)
            login_button.click()

            # Wait for successful login
            WebDriverWait(self.driver, 15).until(
                EC.frame_to_be_available_and_switch_to_it("main")
            )
            print("Successfully logged in!")
            return True

        except Exception as e:
            print(f"Login failed: {e}")
            try:
                print("Attempting to refresh and retry login...")
                self.driver.refresh()
                time.sleep(1)

                login_field = self.driver.find_element(By.NAME, "login")
                password_field = self.driver.find_element(By.NAME, "psw")
                login_button = self.driver.find_element(By.XPATH, "//input[@value='Войти']")

                login_field.send_keys(self.login)
                password_field.send_keys(self.password)
                login_button.click()

                WebDriverWait(self.driver, 15).until(
                    EC.frame_to_be_available_and_switch_to_it("main")
                )
                print("Successfully logged in on retry!")
                return True
            except Exception as retry_e:
                print(f"Retry login also failed: {retry_e}")
                return False

    def navigate_to_battles(self):
        """Navigate to the battles section"""
        print("Navigating to battles...")
        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            try:
                # Return to default content (outside frames)
                self.driver.switch_to.default_content()

                # Find and click on the battles link
                battle_link = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Поединки')]"))
                )
                battle_link.click()
                time.sleep(1)

                # Switch to main frame
                WebDriverWait(self.driver, 15).until(
                    EC.frame_to_be_available_and_switch_to_it("main")
                )

                # Navigate to chaotic battles
                chaotic_link = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Хаотичные')]"))
                )
                chaotic_link.click()
                time.sleep(1)

                print("Successfully navigated to chaotic battles!")
                return True

            except (TimeoutException, StaleElementReferenceException) as e:
                attempts += 1
                print(f"Navigation attempt {attempts}/{max_attempts} failed.")
                if attempts < max_attempts:
                    print("Retrying navigation...")
                    time.sleep(1)
                    try:
                        self.driver.refresh()
                        time.sleep(1)
                    except:
                        pass
                else:
                    print("Failed to navigate after multiple attempts")
                    return False
            except Exception as e:
                print(f"Unexpected error in navigation: {e}")
                return False

    def submit_battle_request(self):
        """Submit a request for a chaotic battle"""
        print("Submitting battle request...")
        attempts = 0
        max_attempts = 3

        # Import captcha handler here to avoid circular imports
        from captcha import solve_captcha

        while attempts < max_attempts:
            try:
                # Check battle state first to see if we're already in a battle
                battle_state = self.check_battle_state()
                if battle_state == 'battle_ready':
                    print("Battle is already in progress. Skipping battle request.")
                    return True

                # Click on submit request button
                submit_request_button = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@value='Подать заявку на хаотичный бой']"))
                )
                submit_request_button.click()
                time.sleep(1)

                # Check for captcha
                try:
                    captcha_elements = self.driver.find_elements(By.XPATH,
                                                                 "//img[contains(@src, 'show_reg_img/security_battle.php')]")

                    if captcha_elements:
                        # Captcha is present, solve it
                        captcha_result = solve_captcha(self.driver)
                        if not captcha_result:
                            print("Failed to solve captcha")
                            return False

                    # Look for the final submit button
                    final_submit_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@name='open'][@value='Подать заявку']"))
                    )
                    final_submit_button.click()
                    time.sleep(1)

                    # Check for incorrect confirmation code message
                    incorrect_code_elements = self.driver.find_elements(By.XPATH,
                                                                        "//b[contains(text(), 'Неправильный код подтверждения')]")
                    if incorrect_code_elements:
                        print("Incorrect confirmation code detected. Restarting battle request process.")
                        return False

                    # Additional check to confirm battle state after submission
                    time.sleep(3)  # Give some time for the battle to start
                    battle_state = self.check_battle_state()

                    if battle_state == 'battle_ready':
                        print("Battle request submitted successfully!")
                        return True
                    elif battle_state == 'request_failed':
                        print("Battle request failed. Retrying...")
                        attempts += 1
                        continue

                except TimeoutException:
                    # Check battle state again if timeout occurs
                    battle_state = self.check_battle_state()
                    if battle_state == 'battle_ready':
                        print("Battle started despite submission issues!")
                        return True

                    # If no battle ready, continue with standard submission
                    try:
                        final_submit_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//input[@name='open'][@value='Подать заявку']"))
                        )
                        final_submit_button.click()
                        time.sleep(1)
                    except:
                        pass

            except Exception as e:
                print(f"Battle request attempt {attempts + 1}/{max_attempts} failed.")

                # Check battle state after exception
                battle_state = self.check_battle_state()
                if battle_state == 'battle_ready':
                    print("Battle is already in progress despite exception!")
                    return True

                attempts += 1
                time.sleep(1)

        print("Failed to submit battle request after multiple attempts")
        return False

    def check_battle_state(self):
        print("Checking battle state...")
        """
        Check the current battle state.

        Returns:
        - 'request_failed': Request button is present, meaning battle request was not successful
        - 'waiting': No battle indicators or request button
        - 'battle_ready': Battle indicators or attack button are present
        """
        try:
            # Check for battle request button (state 1)
            request_buttons = self.driver.find_elements(By.XPATH, "//input[@value='Подать заявку на хаотичный бой']")
            if request_buttons and request_buttons[0].is_displayed():
                print("Battle request button found. Request likely failed.")
                return 'request_failed'

            # Battle indicators from wait_for_battle_to_start method (state 2 and 3)
            battle_indicators = [
                "//button[contains(text(),'Вперёд')]",  # Attack button
                "//img[contains(@src,'pet_unleash.gif')]",  # Pet unleash button
                "//img[@src='https://......gif']"  # Battle refresh indicator
            ]

            # Check for any battle indicators
            for indicator in battle_indicators:
                elements = self.driver.find_elements(By.XPATH, indicator)
                if elements and elements[0].is_displayed():
                    print("Battle indicators found. Battle is ready.")
                    return 'battle_ready'

            # If no request button or battle indicators found (state 2)
            print("Waiting for battle. No indicators found.")
            return 'waiting'

        except Exception as e:
            print(f"Error checking battle state: {e}")
            return 'waiting'

    def wait_for_battle_to_start(self):
        """Wait for the battle to start with enhanced state checking"""
        print("Waiting for battle to start...")
        max_attempts = 10
        attempt = 0

        while attempt < max_attempts:
            try:
                battle_state = self.check_battle_state()

                if battle_state == 'request_failed':
                    print("Battle request failed. Resubmitting request.")
                    return False

                if battle_state == 'battle_ready':
                    print("Battle is ready!")
                    return True

                # If waiting, refresh and continue waiting
                print(f"Waiting for battle... Attempt {attempt + 1}/{max_attempts}")
                self.driver.refresh()
                attempt += 1
                time.sleep(random.uniform(2, 3))

            except Exception as e:
                print(f"Error while waiting for battle: {e}")
                time.sleep(1)
                attempt += 1

        print("Maximum refresh attempts reached. Battle did not start.")
        return False
    def unleash_pet(self):
        """Click on the unleash pet button"""
        print("Unleashing pet...")
        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            try:
                pet_buttons = self.driver.find_elements(By.XPATH, "//img[contains(@src,'pet_unleash.gif')]")
                if pet_buttons and pet_buttons[0].is_displayed():
                    pet_buttons[0].click()
                    print("Pet unleashed!")
                    return True
                else:
                    print(f"Pet button not found. Attempt {attempts + 1}/{max_attempts}")

                    # Check if we're already in a battle
                    attack_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(),'Вперёд')]")
                    if attack_buttons and attack_buttons[0].is_displayed():
                        print("Already in battle, no need to unleash pet!")
                        return True

                attempts += 1
                time.sleep(1)

            except Exception as e:
                print(f"Failed to unleash pet: {e}")
                attempts += 1
                time.sleep(1)

        print("Failed to unleash pet after multiple attempts")
        # Continue anyway as the pet might be optional
        return True

    def battle_cycle(self):
        """Execute the battle cycle of attacking repeatedly"""
        print("Starting battle cycle...")
        max_cycles = 300
        cycle = 0
        consecutive_errors = 0
        max_consecutive_errors = 5
        no_interaction_count = 0
        max_no_interaction = 3

        while cycle < max_cycles and consecutive_errors < max_consecutive_errors:
            try:
                # Check for "return" button first (battle ended)
                return_buttons = self.driver.find_elements(By.XPATH,
                                                           "//button[@name='back_menu_down'] | //input[@value='Ок'] | //a[contains(text(), 'Вернуться')]")

                if return_buttons and return_buttons[0].is_displayed() and return_buttons[0].is_enabled():
                    print("Battle ended. Returning to menu.")
                    return_buttons[0].click()
                    return True

                # Look for attack button
                attack_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(),'Вперёд')]")

                if attack_buttons and attack_buttons[0].is_displayed() and attack_buttons[0].is_enabled():
                    print(f"Attacking... Cycle {cycle + 1}/{max_cycles}")
                    attack_buttons[0].click()
                    time.sleep(random.uniform(0.5, 0.1))
                    consecutive_errors = 0
                    no_interaction_count = 0
                else:
                    # Look for refresh button with specific image
                    refresh_buttons = self.driver.find_elements(By.XPATH,
                                                                "//img[@src='https://.....gif']")

                    if refresh_buttons and refresh_buttons[0].is_displayed():
                        print("Refreshing battle...")
                        refresh_buttons[0].click()
                        time.sleep(5)  # моя удлиненная задержка!
                        consecutive_errors = 0
                        no_interaction_count = 0
                    else:
                        print("No interaction elements found.")
                        no_interaction_count += 1

                        # If unable to interact for several attempts, return False to restart cycle
                        if no_interaction_count >= max_no_interaction:
                            print("No interaction elements found for several attempts. Ending battle cycle.")
                            return False

                cycle += 1

            except StaleElementReferenceException:
                print("Element became stale. Refreshing...")
                consecutive_errors += 1
                try:
                    self.driver.refresh()
                    time.sleep(1)
                except:
                    pass

            except Exception as e:
                print(f"Error in battle cycle.")
                consecutive_errors += 1
                print(f"Consecutive errors: {consecutive_errors}/{max_consecutive_errors}")
                time.sleep(1)

                # Try to refresh if we have multiple errors
                if consecutive_errors >= 3:
                    try:
                        self.driver.refresh()
                        time.sleep(1)
                    except:
                        pass

        if consecutive_errors >= max_consecutive_errors:
            print("Too many consecutive errors. Ending battle cycle.")
        else:
            print("Maximum battle cycles reached.")
        return False

    def collect_bonuses(self):
        """Click on pension bonus and halva coin buttons if they exist"""
        print("Collecting bonuses...")
        attempts = 0
        max_attempts = 1
        bonuses_found = False

        while attempts < max_attempts:
            try:
                # Try to find pension bonus button
                pension_buttons = self.driver.find_elements(By.XPATH, "//input[@value='Получить бонус!']")
                if pension_buttons:
                    pension_buttons[0].click()
                    print("Pension bonus collected!")
                    bonuses_found = True
                    time.sleep(0.5)

                # Try to find halva coin button
                halva_buttons = self.driver.find_elements(By.XPATH, "//input[@value='Получить монетку!']")
                if halva_buttons:
                    halva_buttons[0].click()
                    print("Halva coin collected!")
                    bonuses_found = True
                    time.sleep(0.5)

                # Try to find button_5ekr
                button_5ekr = self.driver.find_elements(By.XPATH, "//input[@value='Получить монетку!']")
                if button_5ekr:
                    button_5ekr[0].click()
                    print("5 ekr coin collected!")
                    bonuses_found = True
                    time.sleep(0.5)

                # If we found and clicked at least one button, consider it successful
                if bonuses_found:
                    return True

                # If no buttons found, increment attempts
                print(f"No bonus buttons found. Attempt {attempts + 1}/{max_attempts}")
                attempts += 1
                time.sleep(1)

            except Exception as e:
                print(f"Failed to collect bonuses: {e}")
                attempts += 1
                time.sleep(1)

        # Continue even if we didn't find any bonus buttons
        print("No bonuses available or failed to collect after multiple attempts")
        return True


    def game_loop(self):
        """Main game loop that runs the entire process"""
        try:
            self.initialize_driver()

            if not self.login_to_game():
                print("Failed to login. Terminating bot.")
                return

            while True:  # Бесконечный цикл с явными условиями выхода
                try:
                    if not self.navigate_to_battles():
                        print("Failed to navigate to battles. Retrying...")
                        time.sleep(1)
                        continue

                    if not self.submit_battle_request():
                        print("Failed to submit battle request. Retrying...")
                        time.sleep(1)
                        continue

                    if not self.wait_for_battle_to_start():
                        print("Battle didn't start. Restarting from battles page...")
                        continue

                    self.unleash_pet()  # Continue even if pet unleash fails

                    if not self.battle_cycle():  # Если battle_cycle возвращает False, начинаем новый цикл
                        print("Battle cycle completed or failed. Starting new cycle...")

                    time.sleep(2)  # Моя увеличенная задержка при загрузке главного меню

                    self.collect_bonuses()  # Collect bonuses if available
                    time.sleep(1)  # Wait 1ms after collecting bonuses

                except Exception as cycle_error:
                    print(f"Error in game cycle: {cycle_error}")
                    time.sleep(1)

                    # Try to recover by refreshing
                    try:
                        self.driver.refresh()
                        time.sleep(1)
                    except:
                        pass

        except KeyboardInterrupt:
            print("Bot terminated by user.")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                print("Webdriver closed.")


if __name__ == "__main__":
    # Replace with your actual login credentials
    LOGIN = "..."
    PASSWORD = "..."

    bot = bot(LOGIN, PASSWORD)
    bot.game_loop()