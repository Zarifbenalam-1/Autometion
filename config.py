# Configuration file for Sheet-to-Whisk Automation
# Edit these values to customize the automation for your needs

# Google Sheets URL - Replace with your sheet URL
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"

# Google Labs Whisk URL - Usually doesn't need to change
WHISK_URL = "https://labs.google/fx/tools/whisk/project/"

# Chrome profile storage location
# Windows: "C:\\Users\\YOUR_USERNAME\\selenium-automation-profile"
# Linux/Mac: "/home/YOUR_USERNAME/selenium-automation-profile"
CHROME_PROFILE_PATH = "./selenium-automation-profile"

# Automation Settings
MAX_EMPTY_CELLS = 3  # Stop after this many consecutive empty cells
WAIT_AFTER_SUBMIT = 2  # Seconds to wait after submitting each prompt
WAIT_FOR_POPUP = 3  # Seconds to wait if "Please wait" popup appears
SHORT_WAIT = 0.3  # Short wait between actions (seconds)

# Browser Settings
START_MAXIMIZED = True  # Open browser in full screen
HEADLESS = False  # Set to True for background operation (may break clipboard)

# Advanced Settings
ENABLE_LOGGING = False  # Save logs to file
LOG_FILE = "automation.log"
SCREENSHOT_ON_ERROR = False  # Save screenshot when errors occur
