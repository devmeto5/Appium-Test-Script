import logging
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions import pointer_input
import os
import time

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_mobile_application():
    logging.info("Starting mobile application test")
    driver = None  # Initialize driver as None
    try:
        # Configure Appium options
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.platform_version = "11.0"  # Make sure this matches your emulator version
        options.device_name = "Android Emulator"  # Make sure this matches your device name
        options.app = r"/path/to/your/app.apk"  # Path to your APK file
        options.app_package = "com.example.app"  # Replace with your app package
        options.app_activity = "com.example.app.MainActivity"  # Replace with your app activity

        # Initialize the driver
        driver = AppiumWebDriver(command_executor="http://localhost:4723", options=options)
        logging.info("Appium driver initialized")

        # Explicit wait for the main screen to load
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Start")')))

        # Take a screenshot for debugging
        screenshot_path = os.path.join(os.getcwd(), "debug_screenshot_before_click.png")
        driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot saved at {screenshot_path}")

        # Use UiAutomator to find and click the 'Start' button
        try:
            button = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Start")')
            button.click()
            logging.info("Clicked the 'Start' button using UiAutomator")
        except NoSuchElementException as e:
            logging.error(f"Failed to find and click the 'Start' button using UiAutomator: {e}")
            return

        # Explicit wait for the popup with the "Continue" button
        try:
            continue_button = wait.until(EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Continue")')
            ))
            continue_button.click()
            logging.info("Clicked the 'Continue' button on the popup")
        except TimeoutException as e:
            logging.error(f"Timed out waiting for the 'Continue' button: {e}")
            return

        # Explicit wait for the "Deny" button
        try:
            deny_button = wait.until(EC.element_to_be_clickable(
                (AppiumBy.XPATH, "//android.widget.Button[@text='Deny']")
            ))
            deny_button.click()
            logging.info("Clicked the 'Deny' button on the popup")
        except TimeoutException as e:
            logging.error(f"Timed out waiting for the 'Deny' button: {e}")
            return

        # Explicit wait for the phone number input field
        try:
            phone_input = wait.until(EC.presence_of_element_located(
                (AppiumBy.CLASS_NAME, "android.widget.EditText")
            ))

            # Enter a phone number
            phone_input.send_keys("+1 1234567890")  # Replace with the desired phone number
            logging.info("Entered phone number into the input field")

            # Hide the virtual keyboard
            driver.hide_keyboard()
            logging.info("Keyboard hidden")
        except TimeoutException as e:
            logging.error(f"Timed out waiting for the phone number input field: {e}")
            return

        # Take a screenshot before clicking the arrow button
        screenshot_before_arrow = os.path.join(os.getcwd(), "debug_screenshot_before_arrow.png")
        driver.save_screenshot(screenshot_before_arrow)
        logging.info(f"Screenshot before finding arrow button saved at {screenshot_before_arrow}")

        # Save the page source for debugging
        page_source = driver.page_source
        page_source_path = os.path.join(os.getcwd(), "page_source_before_arrow.xml")
        with open(page_source_path, "w", encoding="utf-8") as f:
            f.write(page_source)
        logging.info(f"Page source saved at {page_source_path}")

        # Click the arrow button to continue
        try:
            # Attempt to find the button using UiAutomator
            arrow_button = wait.until(EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Next")')
            ))
            arrow_button.click()
            logging.info("Clicked the arrow button using UiAutomator with textContains 'Next'")
        except (TimeoutException, NoSuchElementException) as e:
            logging.error(f"Failed to click the arrow button using UiAutomator: {e}")

            # Attempt to find the button using XPATH
            try:
                arrow_button = wait.until(EC.element_to_be_clickable(
                    (AppiumBy.XPATH, "//android.widget.Button[contains(@content-desc, 'Next')]")
                ))
                arrow_button.click()
                logging.info("Clicked the arrow button using XPATH with content-desc containing 'Next'")
            except (TimeoutException, NoSuchElementException) as e:
                logging.error(f"Failed to click the arrow button using XPATH: {e}")

                # Use W3C Actions to tap on the arrow button coordinates
                try:
                    size = driver.get_window_size()
                    width = size['width']
                    height = size['height']

                    # Define coordinates for the arrow button — bottom right of the screen, above the keyboard
                    x = int(width * 0.9)
                    y = int(height * 0.9)

                    actions = ActionChains(driver)
                    touch = pointer_input.PointerInput(interaction.POINTER_TOUCH, "touch")

                    actions.w3c_actions.add_action(
                        touch.create_pointer_move(duration=0, x=x, y=y, origin='viewport')
                    )
                    actions.w3c_actions.add_action(
                        touch.create_pointer_down(button=0)
                    )
                    actions.w3c_actions.add_action(
                        touch.create_pointer_up(button=0)
                    )
                    actions.perform()
                    logging.info("Tapped on the arrow button using W3C Actions")
                except Exception as touch_e:
                    logging.error(f"Failed to tap on the arrow button using W3C Actions: {touch_e}")
                    return

        # Take a screenshot after clicking the arrow button
        screenshot_path_after_phone = os.path.join(os.getcwd(), "debug_screenshot_after_phone.png")
        driver.save_screenshot(screenshot_path_after_phone)
        logging.info(f"Screenshot saved at {screenshot_path_after_phone}")

        # Additional steps after clicking the arrow button can be added here
        # For example, handling subsequent screens or entering more data

    except Exception as e:
        logging.error(f"An error occurred in mobile application test: {e}")
    finally:
        # Ensure the driver is closed even if an error occurs
        if driver:
            driver.quit()
            logging.info("Appium driver closed for mobile application test")
        else:
            logging.info("Appium driver was not initialized.")

if __name__ == "__main__":
    test_mobile_application()
