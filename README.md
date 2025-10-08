# Autometion - Google Sheets to Whisk Automation

A Python automation tool that automatically copies prompts from Google Sheets and submits them to Google Labs Whisk for AI image generation.

## 🎯 What Does This System Do?

This automation tool:
1. **Opens a Chrome browser** with two tabs
2. **Reads prompts** from your Google Sheet (one cell at a time)
3. **Navigates to Google Labs Whisk** (AI image generator)
4. **Pastes each prompt** into Whisk's input field
5. **Submits the prompt** by pressing Enter
6. **Moves to the next row** automatically
7. **Repeats** until it finds 3 consecutive empty cells
8. **Handles errors** gracefully (popup warnings, missing elements, etc.)

### Real-World Use Case
If you have 100 AI image prompts in a Google Sheet and want to generate images for all of them using Whisk, this tool automates the tedious copy-paste process. It saves hours of manual work!

## 📁 What Files Are Stored?

### Chrome Profile Data
- **Location**: `C:\Users\jubay\selenium-automation-profile\` (Windows) or `~/selenium-automation-profile/` (Linux/Mac)
- **Contents**: Browser cookies, login sessions, cache
- **Purpose**: Keeps you logged into Google so you don't have to authenticate every time

### No Other Storage
- **No databases**: Everything happens in real-time
- **No logs**: Terminal output only (can be added if needed)
- **No screenshots**: System doesn't save any images (you download manually from Whisk)

## 🚀 How to Make This Your Own

### Step 1: Install Python
```bash
# Check if Python is installed
python --version

# Should show Python 3.8 or higher
```

### Step 2: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

### Step 3: Customize for Your Needs

#### Change Google Sheet URL
Edit line 31 in `automation_sheet_to_whisk.py`:
```python
driver.get("YOUR_GOOGLE_SHEET_URL_HERE")
```

**How to get your Sheet URL:**
1. Open your Google Sheet
2. Copy the URL from browser address bar
3. Paste it in the code

#### Change Profile Storage Location
Edit line 14 in `automation_sheet_to_whisk.py`:
```python
# Windows
user_data_dir = "C:\\Users\\YOUR_USERNAME\\selenium-automation-profile"

# Linux/Mac
user_data_dir = "/home/YOUR_USERNAME/selenium-automation-profile"
```

#### Adjust Empty Cell Threshold
Edit line 54 in `automation_sheet_to_whisk.py`:
```python
max_empty_cells = 5  # Stop after 5 empty cells instead of 3
```

#### Change Wait Times
If your internet is slow, increase wait times:
```python
time.sleep(5)  # Wait 5 seconds instead of 3
```

### Step 4: Run the Automation
```bash
python automation_sheet_to_whisk.py
```

### Step 5: First-Time Setup
1. **Browser will open** - A Chrome window appears
2. **Google Sheets tab** - You may need to log in to Google
3. **Whisk tab** - You may need to log in to Google Labs
4. **Let it run** - Once logged in, the automation starts

### Step 6: Stop the Automation
- Press `Ctrl+C` in the terminal to stop anytime
- Or wait for it to finish when it finds 3 empty cells

## 🛠️ Customization Ideas

### 1. Add Logging to File
```python
import logging
logging.basicConfig(filename='automation.log', level=logging.INFO)
logging.info(f"Processed cell {cell_count}")
```

### 2. Multi-Column Support
Currently reads column A only. To read column B:
```python
actions.key_down(Keys.CONTROL).send_keys(Keys.HOME).key_up(Keys.CONTROL).perform()
actions.send_keys(Keys.RIGHT).perform()  # Move to column B
```

### 3. Screenshot Each Result
```python
driver.save_screenshot(f"result_{cell_count}.png")
```

### 4. Email Notification When Done
```python
import smtplib
# Add email sending code at the end
```

### 5. Config File for Settings
Create `config.yaml`:
```yaml
google_sheet_url: "https://docs.google.com/..."
whisk_url: "https://labs.google/fx/tools/whisk/project/"
max_empty_cells: 3
wait_time: 2
```

## 🔧 Troubleshooting

### "Element not found" Error
- Whisk's UI may have changed
- Update the XPath selectors in lines 78-93

### Browser Doesn't Open
- Check if Chrome is installed
- Try: `pip install --upgrade selenium webdriver-manager`

### "Access Denied" on Google Sheets
- Make sure sheet is public or you're logged in
- The profile stores your login session

### Automation Too Fast/Slow
- Adjust `time.sleep()` values throughout the code
- Increase waits for slow internet
- Decrease waits for fast internet

## 📊 Understanding the Code Flow

```
START
  ↓
Open Chrome with custom profile
  ↓
Navigate to Google Sheets (Tab 1)
  ↓
Open Whisk in new tab (Tab 2)
  ↓
Select cell A1 in Sheets
  ↓
┌─────────────────────────────┐
│ LOOP (for each row)         │
│  1. Copy cell (Ctrl+C)      │
│  2. Switch to Whisk tab     │
│  3. Find text input field   │
│  4. Paste (Ctrl+V)          │
│  5. Press Enter             │
│  6. Wait for processing     │
│  7. Clear input field       │
│  8. Switch to Sheets tab    │
│  9. Move down (Arrow key)   │
│  10. Check if cell empty    │
│      - If 3 empty → STOP    │
│      - Else → Continue      │
└─────────────────────────────┘
  ↓
Print completion message
  ↓
Wait for user to press Enter
  ↓
Close browser
  ↓
END
```

## 🎓 Learning Resources

### Selenium Basics
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Web Scraping Tutorial](https://realpython.com/modern-web-automation-with-python-and-selenium/)

### XPath Selectors
- [XPath Cheatsheet](https://devhints.io/xpath)
- Use Chrome DevTools: Right-click element → Inspect → Copy XPath

### Chrome DevTools
- Press `F12` in Chrome to inspect webpage elements
- Use "Selector" tool to find element paths

## 📝 License
This project is open-source. Feel free to modify and use for your needs!

## 🤝 Contributing
Have improvements? Create a pull request or open an issue!

---
**Created by analyzing automation workflow from video screenshots**