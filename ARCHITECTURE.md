# System Architecture & Data Flow

## 🏗️ System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTOMETION SYSTEM                         │
└─────────────────────────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │ Selenium │   │  Chrome  │   │  Config  │
    │ WebDriver│   │ Browser  │   │  Files   │
    └──────────┘   └──────────┘   └──────────┘
           │               │               │
           └───────────────┼───────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       ┌─────────────┐          ┌─────────────┐
       │ Google      │          │ Google Labs │
       │ Sheets      │          │ Whisk       │
       │ (Source)    │          │ (Target)    │
       └─────────────┘          └─────────────┘
```

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA FLOW                                 │
└─────────────────────────────────────────────────────────────┘

   Google Sheet                      System                      Whisk
  ┌──────────┐                    ┌─────────┐                ┌─────────┐
  │          │                    │         │                │         │
  │  A1: Cat │  ───(Ctrl+C)─────> │ Clipbrd │ ─(Ctrl+V)───> │ [Input] │
  │          │                    │         │                │         │
  │  A2: Dog │                    │ Memory  │                │ [Submit]│
  │          │                    │         │                │         │
  │  A3: ...│                     │ Counter │                │ [Clear] │
  │          │                    │         │                │         │
  │  A4:     │  ─(Check Empty)──> │ Stop?   │                │ [Wait]  │
  │          │                    │         │                │         │
  └──────────┘                    └─────────┘                └─────────┘
       ▲                                │                          │
       │                                │                          │
       └────────────(Arrow Down)────────┘                          │
                                                                   │
       ┌────────────────────────────────────────────────────────────┘
       │
       └─────> [Image Generation Starts]
```

## 🔀 Control Flow

```
START
  │
  ├─> [Setup Chrome Driver]
  │     └─> Load profile from disk
  │
  ├─> [Open Browser]
  │     ├─> Tab 1: Google Sheets
  │     └─> Tab 2: Whisk
  │
  ├─> [Initialize Variables]
  │     ├─> cell_count = 1
  │     └─> empty_cells_count = 0
  │
  └─> [Main Loop] ◄──────────────┐
        │                        │
        ├─> Read cell A{n}       │
        │     └─> Ctrl+C         │
        │                        │
        ├─> Switch to Whisk      │
        │                        │
        ├─> Find input field     │
        │     ├─> Try XPath #1   │
        │     ├─> Try XPath #2   │
        │     └─> Try Tag Name   │
        │                        │
        ├─> Paste text           │
        │     └─> Ctrl+V         │
        │                        │
        ├─> [Check if Empty]     │
        │     ├─> Yes: count++   │
        │     │   └─> If count=3 → STOP
        │     └─> No: Submit     │
        │           └─> Enter    │
        │                        │
        ├─> Wait for processing  │
        │     └─> Check popup    │
        │                        │
        ├─> Clear field          │
        │                        │
        ├─> Switch to Sheets     │
        │                        │
        ├─> Move down (Arrow)    │
        │                        │
        └─> cell_count++         │
              │                  │
              └──────────────────┘

STOP
  │
  ├─> Print summary
  │
  ├─> Wait for user (Enter)
  │
  └─> Close browser
```

## 💾 File Storage Structure

```
Project Root
│
├─ automation_sheet_to_whisk.py  ← Main script
├─ config.py                     ← Settings
├─ requirements.txt              ← Dependencies
├─ README.md                     ← Full guide
├─ QUICKSTART.md                 ← Quick start
│
└─ selenium-automation-profile/  ← Chrome profile storage
   ├─ Default/
   │  ├─ Cookies                 ← Login sessions
   │  ├─ Local Storage           ← Cached data
   │  └─ Preferences             ← Browser settings
   │
   └─ [Other Chrome data]

Optional (if enabled):
├─ automation.log                ← Execution logs
└─ screenshots/                  ← Error screenshots
   └─ error_001.png
```

## 🔐 Security & Privacy

```
┌─────────────────────────────────────────────────────────┐
│ WHAT'S STORED                                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ ✅ Stored Locally:                                      │
│    • Chrome profile (cookies, sessions)                │
│    • Browser cache                                     │
│    • Login tokens (Google account)                     │
│                                                         │
│ ❌ NOT Stored:                                          │
│    • Your prompts (only in clipboard temporarily)      │
│    • Generated images (stay in Whisk)                  │
│    • Passwords (handled by Chrome)                     │
│    • Personal data (no tracking)                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## ⚡ Performance Characteristics

```
┌─────────────────────────────────────────┐
│ Speed: ~10-15 seconds per prompt        │
├─────────────────────────────────────────┤
│ Breakdown:                              │
│  • Copy from sheet: 0.3s                │
│  • Switch tabs: 0.3s                    │
│  • Find element: 0.5s                   │
│  • Paste text: 0.5s                     │
│  • Submit: 0.1s                         │
│  • Wait for Whisk: 2-3s                 │
│  • Clear field: 0.5s                    │
│  • Move to next: 0.3s                   │
└─────────────────────────────────────────┘

For 100 prompts: ~20-25 minutes total
```

## 🎯 Use Cases

```
1. Bulk AI Image Generation
   Google Sheet → Whisk → Download images

2. Prompt Testing
   Test multiple variations quickly

3. Dataset Creation
   Generate training data for ML models

4. Creative Projects
   Batch process creative ideas

5. Marketing Materials
   Generate multiple ad concepts
```

## 🔧 Extension Points

```
Easy to extend:
├─ Add new data sources
│  └─ Replace Google Sheets with CSV, Excel, Database
│
├─ Add new targets
│  └─ Replace Whisk with ChatGPT, Midjourney, etc.
│
├─ Add preprocessing
│  └─ Modify prompts before submission
│
├─ Add postprocessing
│  └─ Download images, rename files, etc.
│
└─ Add monitoring
   └─ Send notifications, log to cloud, etc.
```
