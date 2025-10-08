from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Setup Chrome options
user_data_dir = "C:\\Users\\jubay\\selenium-automation-profile"
if not os.path.exists(user_data_dir):
    os.makedirs(user_data_dir)

chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# Additional options for better background operation
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu-sandbox")
chrome_options.add_experimental_option("detach", True)  # Keep browser open after script ends

# Initialize driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

try:
    # Open Google Sheets in first tab
    driver.get("https://docs.google.com/spreadsheets/d/1-znij-rdmpYyfHjrrtpmHtscKX7QE-q8Z-EfGlkpU/edit?gid=64971i5q1pjd-64971i5p1")
    
    # Wait for sheets to load
    time.sleep(3)
    
    # Open Whisk in a new tab
    driver.execute_script("window.open('https://labs.google/fx/tools/whisk/project/', '_blank');")
    
    # Store window handles
    sheets_tab = driver.window_handles[0]
    whisk_tab = driver.window_handles[1]
    
    print("Both tabs opened successfully. Starting automation...")
    
    # Wait for both tabs to load properly
    time.sleep(5)
    
    # Switch back to Google Sheets
    driver.switch_to.window(sheets_tab)
    
    # Counter for cells
    cell_count = 1
    empty_cells_count = 0
    max_empty_cells = 3  # Stop after 3 consecutive empty cells
    
    # Initial selection of A1 - Find the first cell directly
    time.sleep(2)
    try:
        # Find the first cell (A1) in Google Sheets
        first_cell = driver.find_element(By.CSS_SELECTOR, "div[role='gridcell']")
        first_cell.click()
        time.sleep(0.5)
    except:
        print("Could not locate first cell, using keyboard shortcut as fallback")
        actions.key_down(Keys.CONTROL).send_keys(Keys.HOME).key_up(Keys.CONTROL).perform()
        time.sleep(1)
    
    while True:
        try:
            print(f"\n--- Processing cell A{cell_count} ---")
            
            # Switch to Google Sheets tab
            driver.switch_to.window(sheets_tab)
            time.sleep(0.30)
            
            # Get the current cell content directly from the active cell
            try:
                # Find the currently selected cell in Google Sheets
                active_cell = driver.find_element(By.CSS_SELECTOR, "div[role='gridcell'][aria-selected='true']")
                cell_text = active_cell.text.strip()
                print(f"Found cell content: '{cell_text[:50]}...'")
            except:
                # Fallback: try to get text from input box if cell is being edited
                try:
                    input_box = driver.find_element(By.CSS_SELECTOR, "input.waffle-cell-editor, textarea.waffle-cell-editor")
                    cell_text = input_box.get_attribute('value') or input_box.text
                    print(f"Found content in input box: '{cell_text[:50]}...'")
                except:
                    # Last resort: use keyboard copy (but focus the window first)
                    print("Using keyboard copy as fallback")
                    driver.switch_to.window(sheets_tab)
                    driver.execute_script("window.focus();")
                    actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
                    time.sleep(0.5)
                    cell_text = None  # We'll paste directly later
            
            # Switch to Whisk tab
            driver.switch_to.window(whisk_tab)
            time.sleep(0.30)
            
            # Find the text input box
            try:
                # Try multiple possible selectors for the text input
                text_input = None
                
                # Try to find by placeholder text
                try:
                    text_input = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Describe your idea or roll the dice for prompt ideas')]")
                except:
                    pass
                
                # If not found, try to find by type and position
                if not text_input:
                    # Clear any existing text using Selenium's clear method
                    text_input.clear()
                    time.sleep(0.25)
                    
                    # Input the text directly using Selenium (no clipboard needed)
                    if cell_text is not None:
                        text_input.send_keys(cell_text)
                        pasted_text = cell_text
                    else:
                        # Fallback to clipboard paste if we couldn't get text directly
                        text_input.send_keys(Keys.CONTROL + 'v')
                        time.sleep(0.50)
                        pasted_text = text_input.get_attribute('value')
                    
                    time.sleep(0.50)
                if text_input:
                    # Click on the input field
                    text_input.click()
                    time.sleep(0.25)
                    
                    # Clear any existing text
                    text_input.send_keys(Keys.CONTROL + 'a')
                    time.sleep(0.25)
                    text_input.send_keys(Keys.DELETE)
                    time.sleep(0.25)
                    
                    # Paste the copied content (Ctrl+V)
                    text_input.send_keys(Keys.CONTROL + 'v')
                    time.sleep(0.50)
                    
                    # Check if we pasted something (not empty)
                    pasted_text = text_input.get_attribute('value')
                    if not pasted_text or pasted_text.strip() == "":
                        print(f"Cell A{cell_count} appears to be empty")
                        empty_cells_count += 1
                        if empty_cells_count >= max_empty_cells:
                            print(f"Encountered {max_empty_cells} consecutive empty cells. Stopping automation.")
                            break
                    else:
                        print(f"Pasted content from cell A{cell_count}: {pasted_text[:50]}...")
                        empty_cells_count = 0  # Reset empty cells counter
                        
                        # Submit by pressing Enter key
                        text_input.send_keys(Keys.ENTER)
                        print("Submitted prompt by pressing Enter")
                        
                        # Check for overload warning and wait if needed
                        time.sleep(0.50)  # Small delay before checking for popup
                        
                        try:
                            # Look for the "Please wait. Processing the requested images" popup
                            overload_popup = None
                            
                            # Try different ways to find the popup message
                            popup_texts = [
                                "Please wait. Loading requested images.",
                                "Please wait",
                                "Processing the requested images",
                                "processing"
                            ]
                            
                            for popup_text in popup_texts:
                                try:
                                    # Look for the popup by text
                        # Clear the text box using Selenium's clear method
                        try:
                            text_input.clear()
                            print("Cleared text box")
                        except:
                            print("Could not clear text box. It might have been cleared automatically")ted images'")
                                print("    Pausing for 3 seconds to let Whisk catch up...")
                                time.sleep(3)
                            else:
                                # Normal processing wait
                                time.sleep(2)
                        
                        except Exception as e:
                            # If we can't check for popup, just use normal wait time
                            print("Could not check for overload popup: {e}")
                            time.sleep(1)
                        
                        # Clear the text box
                        try:
                            text_input.click()
                            text_input.send_keys(Keys.CONTROL + 'a')
                            time.sleep(0.25)
                            text_input.send_keys(Keys.DELETE)
                            print("Cleared text box")
                        except:
                            print("Could not clear text box. It might have been cleared automatically")
                
                else:
                    print("Could not find text input field!")
                    break
            
            except Exception as e:
                print(f"Error processing Whisk input: {e}")
                pass
            
            # Move to next cell - try direct cell selection first
            driver.switch_to.window(sheets_tab)
            try:
                # Try to find and click the next cell directly
                next_cell_selector = f"div[role='gridcell'][data-row='{cell_count}'][data-col='0']"
                next_cell = driver.find_element(By.CSS_SELECTOR, next_cell_selector)
                next_cell.click()
                print(f"Clicked directly on cell A{cell_count + 1}")
            except:
                # Fallback to arrow key navigation
                print("Using arrow key navigation")
                driver.execute_script("window.focus();")  # Ensure window has focus
                actions.send_keys(Keys.DOWN).perform()
            
            time.sleep(0.3)
            cell_count += 1
        
        except KeyboardInterrupt:
            print("\nAutomation interrupted by user")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            cell_count += 1
            continue

    print(f"\n--- Automation completed ---")
    print(f"Processed {cell_count - 1} cells")
    print("\nYou can now download the generated images from Whisk")
    
    input("\nPress Enter to close the browser...")

except Exception as e:
    print(f"Fatal error: {e}")
    input("\nPress Enter to close the browser...")

finally:
    driver.quit()
