# 🚀 Autometion - Quick Start Guide

## What This System Does

**Autometion** automatically copies text prompts from a Google Sheet and submits them to Google Labs Whisk (AI image generator), one by one, until the sheet is empty.

### 🎯 **The Process:**
```
Google Sheet (Column A) → Chrome Automation → Whisk AI → Generated Images
   Row 1: "sunset over mountains"     →   🖼️ Image 1
   Row 2: "futuristic city"           →   🖼️ Image 2  
   Row 3: "cute robot dog"            →   🖼️ Image 3
   ...and so on automatically
```

### ✅ **Key Features:**
- **Works when Chrome is minimized** 
- **You can use other apps while it runs**
- **No keyboard interference with your work**
- **Stops automatically when sheet is empty**
- **Handles Whisk overload warnings**
- **Processes 27+ prompts unattended**

## 📋 Prerequisites

1. **Python 3.7+** installed
2. **Chrome browser** 
3. **Google Sheet** with prompts in Column A
4. **Internet connection**

## 🛠️ Installation

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Your Google Sheet URL
Edit `automation_sheet_to_whisk.py` line 31:
```python
driver.get("https://docs.google.com/spreadsheets/d/YOUR-SHEET-ID/edit")
```

## 🎮 Running the Automation

### Quick Start:
```bash
python automation_sheet_to_whisk.py
```

### What You'll See:
1. **Chrome opens** with 2 tabs (Google Sheets + Whisk)
2. **"Both tabs opened successfully. Starting automation..."**
3. **Processing messages** for each row: `"--- Processing cell A1 ---"`
4. **Progress updates** in terminal
5. **Automatic completion** when done

### 💡 **Pro Tips:**
- **Minimize Chrome** after setup (it keeps working!)
- **Use other apps** freely while it runs
- **Monitor terminal** for progress
- **Let it run overnight** for large sheets

## � Troubleshooting

### Chrome Won't Open:
```bash
# Update Chrome driver
pip install --upgrade webdriver-manager
```

### Script Stops Early:
- Check Google Sheet permissions (must be viewable)
- Verify Whisk website is accessible
- Try running with Chrome visible first

### Keyboard Shortcuts in Other Apps:
- This is fallback mode - check terminal for errors
- Usually resolves itself after a few iterations

**For detailed background operation info, see `BACKGROUND_OPERATION_GUIDE.md`**

**Happy Automating! 🤖✨**
