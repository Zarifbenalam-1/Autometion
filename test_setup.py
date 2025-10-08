#!/usr/bin/env python3
"""
Test script to verify the automation setup
Run this before running the full automation
"""

import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.8+"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} - Need 3.8+")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking dependencies...")
    
    packages = {
        'selenium': 'selenium',
        'webdriver_manager': 'webdriver-manager'
    }
    
    all_installed = True
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"   ✅ {package} - Installed")
        except ImportError:
            print(f"   ❌ {package} - Not installed")
            all_installed = False
    
    return all_installed

def check_chrome():
    """Check if Chrome is installed"""
    print("\n🔍 Checking Chrome browser...")
    try:
        # Try to find Chrome executable
        import shutil
        chrome_paths = [
            'google-chrome',
            'chrome',
            'chromium',
            'chromium-browser',
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
        ]
        
        for path in chrome_paths:
            if shutil.which(path) or __import__('os').path.exists(path):
                print(f"   ✅ Chrome found at: {path}")
                return True
        
        print("   ⚠️  Chrome not found (will try to detect during run)")
        return True  # Don't fail, selenium will try
    except Exception as e:
        print(f"   ⚠️  Could not verify Chrome: {e}")
        return True

def check_config():
    """Check if config file exists and has valid settings"""
    print("\n🔍 Checking configuration...")
    try:
        import config
        
        # Check if Google Sheet URL is set
        if config.GOOGLE_SHEET_URL == "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit":
            print("   ⚠️  Google Sheet URL not configured in config.py")
            print("      Please update GOOGLE_SHEET_URL with your sheet URL")
            return False
        else:
            print(f"   ✅ Google Sheet URL configured")
        
        print(f"   ✅ Max empty cells: {config.MAX_EMPTY_CELLS}")
        print(f"   ✅ Wait time: {config.WAIT_AFTER_SUBMIT}s")
        
        return True
    except Exception as e:
        print(f"   ❌ Error reading config: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("   AUTOMETION - System Check")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Chrome Browser", check_chrome),
        ("Configuration", check_config)
    ]
    
    results = []
    for name, check_func in checks:
        result = check_func()
        results.append(result)
    
    print("\n" + "=" * 60)
    print("   SUMMARY")
    print("=" * 60)
    
    if all(results):
        print("✅ All checks passed! Ready to run automation.")
        print("\n📝 Next steps:")
        print("   1. Make sure you have a Google Sheet with prompts")
        print("   2. Update config.py with your sheet URL")
        print("   3. Run: python automation_sheet_to_whisk.py")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\n📝 Installation help:")
        print("   • Install dependencies: pip install -r requirements.txt")
        print("   • Install Chrome: https://www.google.com/chrome/")
        print("   • Update config.py with your settings")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
