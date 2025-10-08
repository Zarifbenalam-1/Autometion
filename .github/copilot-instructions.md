# Copilot Instructions for Autometion

## Project Overview
**Autometion** is a Python-based Selenium automation tool that copies prompts from a Google Sheet and sequentially submits them to Google Labs Whisk (AI image generation tool). The system runs with a visible Chrome browser and handles tab switching, clipboard operations, and smart empty-cell detection.

## Architecture

### Tech Stack
- **Language**: Python 3.13
- **Framework**: Selenium WebDriver 4.x
- **Browser**: Chrome (managed via webdriver-manager)
- **Automation**: ActionChains for keyboard shortcuts
- **No API dependencies**: Direct browser automation (no Google Sheets API)

### Key Components
```
Main Script: "Automation for G Sheet To Whisk Data Copy And Paste.py"
├── Browser Setup: Custom Chrome profile with automation exclusions
├── Tab Management: Switches between Google Sheets & Whisk tabs
├── Element Locator: Multiple fallback strategies (XPath, TAG_NAME)
├── Clipboard Operations: Uses Ctrl+C/V for copy-paste
└── Loop Controller: Processes until 3 consecutive empty cells
```

## Critical Workflows

### Running the Automation
```bash
python "Automation for G Sheet To Whisk Data Copy And Paste.py"
```
- Browser opens in **visible mode** (not headless) - required for clipboard operations
- Manual interruption: Press `Ctrl+C` in terminal

### Configuration Points
1. **Google Sheet URL** (line ~31): Hardcoded spreadsheet link
2. **Whisk URL** (line ~37): `https://labs.google/fx/tools/whisk/project/`
3. **User Profile Path** (line ~14): `C:\Users\jubay\selenium-automation-profile`
4. **Empty Cell Threshold** (line ~54): Stops after 3 consecutive empty cells

## Project-Specific Patterns

### Element Location Strategy
The script uses **defensive selector cascading** to handle Whisk's dynamic UI:
```python
# 1. Try placeholder-based XPath
# 2. Fallback to type-based XPath
# 3. Final fallback to TAG_NAME
```
This pattern is essential because Whisk's input field structure varies.

### Smart Loop Termination
- Tracks `empty_cells_count` and `max_empty_cells = 3`
- Prevents infinite loops when sheet data ends
- Does NOT rely on explicit row count

### Timing Philosophy
- Short waits (0.25-0.5s) between actions to mimic human behavior
- Longer waits (2-3s) for page loads and processing
- No explicit Selenium waits (uses `time.sleep()`)

### Error Handling Approach
- Try/except around element finding (fails gracefully)
- Popup detection for "Please wait. Processing the requested images"
- Keyboard interrupt handling with cleanup

## Integration Points

### Google Sheets
- **Access Method**: Direct browser navigation (public/authenticated sheet)
- **Data Reading**: Clipboard copy via `Ctrl+C` on selected cell
- **Navigation**: Arrow keys (`Keys.DOWN`) to move between rows
- **No API calls**: Avoids OAuth complexity

### Google Labs Whisk
- **Input Method**: Text input field (multiple selector strategies)
- **Submission**: `Keys.ENTER` to trigger processing
- **Popup Handling**: Detects "overload" warnings and waits
- **No result scraping**: User manually downloads images

## Development Notes

### Why No Google Sheets API?
The current approach uses browser automation instead of Sheets API to:
- Avoid OAuth2 authentication setup
- Simplify deployment (no credentials.json needed)
- Handle private sheets if user is already logged in

### ChromeDriver Management
Uses `webdriver-manager` for automatic driver installation:
```python
from webdriver_manager.chrome import ChromeDriverManager
service=Service(ChromeDriverManager().install())
```
No manual driver downloads needed.

### Known Limitations
1. Clipboard operations require visible browser (cannot run headless)
2. Timing-based waits (not dynamic element waits)
3. Single-column processing only (always column A)
4. No resume capability (starts from beginning)

## Future Enhancement Areas
- Add configuration file for URLs and settings
- Implement explicit waits (WebDriverWait) instead of time.sleep()
- Add logging to file for debugging
- Support multi-column processing
- Add resume/checkpoint functionality
- Create requirements.txt for dependency management

---
**Last Updated**: Based on working implementation as of screenshot analysis
