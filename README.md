# 🚀 EveryClicker | Advanced Mouse & Keyboard Autoclicker

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![GUI: CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-darkgreen.svg)](https://github.com/tomsimons/CustomTkinter)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()

**EveryClicker** is a premium, lightweight, and modern utility designed to automate mouse clicks and keyboard keystrokes on Windows. Built with a sleek dark-mode user interface using CustomTkinter, it features a classic clicker, a highly advanced silent clicker with randomized/weighted distributions, and a low-level macro recording/playback engine.

---

## ✨ Key Features

### 🖱️ 1. Classic Clicker
- **Dual Simulation Modes**: Automate either mouse clicks (Left, Right, Middle, Single/Double clicks) or keyboard keystrokes.
- **High-Precision Timing**: Set custom delay intervals in milliseconds (ms) with dynamic real-time clicks-per-second (CPS) conversion.
- **Preset Configurations**: Quickly save, load, or delete presets inline without annoying popups.

### 🤫 2. Silent Clicker (Advanced Humanizer)
- **Randomized Intervals**: Generate random intervals between a minimum (A) and maximum (B) speed to mimic human behaviors.
- **Weighted Distributions (Biased)**: 
  - Define a split threshold limit (C).
  - Target either above or below the threshold with a target percentage chance (P%).
  - Perfect for anti-cheat bypasses and natural-looking interactions.
- **Zero-Boundary Protection**: Seamlessly auto-adjusts limits to prevent division-by-zero crashes.

### 📼 3. Macro Recorder & Playback
- **Low-Level Hooking**: Record actual keyboard event sequences (Key Down / Key Up events) with millisecond-accurate delay tracking.
- **Timing Flexibility**: Replay recorded events in real-time or apply a fixed delay between keystrokes.
- **Anti-Lockup Protection**: Automatic safety release of all physical keys upon stopping or exiting macro execution.

### ⚙️ 4. Global Settings & UX
- **Global Toggle Hotkey**: Bind a global shortcut key (default: `F6`) to start/stop the active engine anytime, even when the application is minimized.
- **Multilingual Support**: Fully translated into **English**, **Français**, and **Español** (detects preferences and persists settings dynamically).
- **Responsive Layout**: Resizable window with DPI scaling and safety constraints (`740x670` minimum size) to prevent layout clipping.

---

## 🛠️ Installation & Setup

### Option A: Standalone Executable (Recommended)
You do not need Python installed to run the application. Simply download the standalone executable:
1. Go to the `dist/` directory or download `everyclicker.exe`.
2. Double-click to run!

### Option B: Run from Source Code
1. Clone this repository:
   ```bash
   git clone https://github.com/TheoOrigin/EveryClicker.git
   cd EveryClicker
   ```
2. Install dependencies:
   ```bash
   pip install customtkinter pillow
   ```
3. Run the application:
   ```bash
   python everyclicker.py
   ```

---

## 🏗️ Building Standalone Executable
To package the project yourself into a standalone `.exe` using PyInstaller:
```bash
pip install pyinstaller
python -m PyInstaller --onefile --noconsole --icon=logo.ico --add-data "logo.ico;." --add-data "logo.png;." --add-data "<path_to_customtkinter>;customtkinter/" everyclicker.py
```
*(Replace `<path_to_customtkinter>` with the installation path of your `customtkinter` site-packages folder)*

---

## 🎛️ Default Settings
- **Language**: English (`en`)
- **Default Click Presets**:
  - `Minecraft Clicker (12 CPS)`: Mouse, Left click, Single, 83.3 ms, Infinite duration.
  - `Auto Key E (10ms)`: Keyboard, key `E`, 10.0 ms, Infinite duration.
- **Default Stop Mode**: Infinite (`Infini`) for all tabs.

---

## 📜 License
Developed by **@TheoOrigin**
