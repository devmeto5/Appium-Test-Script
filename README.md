# README Instructions for Selenium and Appium Test Script

## Overview
This project contains an end-to-end (E2E) automated test script for a mobile application using Appium and Selenium WebDriver. The script is intended to test user interactions such as button clicks, pop-up handling, and phone number input on an Android emulator

## Prerequisites
- Python 3.x installed
- Appium Server installed and running on `http://localhost:4723`
- Android Emulator installed and running
- The APK file of the application to be tested
- Java Development Kit (JDK) installed

### Python Dependencies
Make sure you have installed the required Python packages. You can install them using the command:

```sh
pip install Appium-Python-Client selenium
```

## Setup
1. **Clone the Repository**
   ```sh
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Configure Appium Options**
   - Update the script to point to the correct APK file path:
     ```python
     options.app = r"/path/to/your/app.apk"
     ```
   - Replace `options.app_package` and `options.app_activity` with the correct values for your application.

3. **Run Appium Server**
   Ensure the Appium server is running before executing the script:
   ```sh
   appium
   ```

4. **Run the Test Script**
   Execute the script using the following command:
   ```sh
   python test_script.py
   ```

## Script Overview
The script performs the following steps:
1. Initializes the Appium WebDriver with the desired capabilities.
2. Waits for the main screen of the app to load and clicks the "Start" button.
3. Handles pop-ups such as "Continue" and "Deny".
4. Inputs a phone number and clicks on the arrow button to continue.
5. Takes screenshots and saves the page source for debugging purposes.

### Key Features
- **Logging**: The script uses Python's `logging` module to provide detailed information on each step.
- **Explicit Waits**: Utilizes Selenium's `WebDriverWait` to wait for elements to be present before interacting.
- **Error Handling**: Handles `TimeoutException` and `NoSuchElementException` to prevent script crashes.

## Debugging
- **Screenshots**: Screenshots are saved at various stages of the test to help with debugging.
- **Page Source**: The XML page source is saved for troubleshooting issues related to locating elements.

## Customization
- **Adjust Timeouts**: You can adjust the timeout values for `WebDriverWait` if your application takes longer to load certain screens.
- **Change Locators**: Modify locators (e.g., `AppiumBy.XPATH`, `AppiumBy.ANDROID_UIAUTOMATOR`) based on the actual elements in your application.

## Troubleshooting
- **Appium Server Not Running**: Ensure the Appium server is running on `http://localhost:4723`.
- **Incorrect Locators**: Verify that the locators used in the script are correct by using Appium Inspector to explore the elements of your app.
- **Element Not Found**: If elements are not found, increase the timeout or modify the locator strategy.

## Contributing
Feel free to submit issues or contribute to the project by creating pull requests.

## License
This project is licensed under the MIT License.

