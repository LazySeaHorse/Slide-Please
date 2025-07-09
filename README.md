# Slide Please!

A simple Python application that allows you to advance slides in presentations using a custom voice command. Built with Tkinter for the UI and Picovoice Porcupine for lightweight, local keyword detection.

### Features

[![rhtgdf.png](https://i.postimg.cc/0Qjv2jYD/rhtgdf.png)](https://postimg.cc/t1KwBXm4)

- Custom voice keyword detection
- Multiple slide advancement key options
- Lightweight and cross-platform

## Prerequisites

- Python
- Picovoice Account (free tier available)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/LazySeaHorse/Slide-Please.git
cd Slide-Please
```

2. Create a virtual environment and install required dependencies:
```bash
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

pip install tkinter pyautogui pvporcupine pyaudio
```

> [!NOTE]
> Always activate the virtual environment with `.venv\Scripts\activate` or the Linux/macOS equivalent
> I know this is a pain. But this _is_ a proof-of-conept typa thing ¯\_(ツ)_/¯

## Picovoice Setup (Step-by-Step)

1. Go to [Picovoice Console](https://console.picovoice.ai/)
2. Create a free account
3. Navigate to "Porcupine" in the dashboard
4. Click "Create Keyword"
5. Choose your custom wake word (e.g., "next slide please")
6. Select your target platform (usually Linux/Mac/Windows)
7. Download the `.ppn` keyword file
8. Rename the file to `next_slide_please.ppn`
9. Place the `.ppn` file in the same directory as the script
10. Copy your Picovoice Access Key from the console

## Configuration

Open the script and replace:
```python
PICOVOICE_ACCESS_KEY = "YOUR_API_KEY"  # Paste your Picovoice access key here
```

## Usage

1. Run the script:
```bash
python slide_please.py
```

2. Select the key you want to simulate (Right Arrow by default)
3. Click "Start Listening"
4. Say your custom wake word to advance slides

## Customization

- Change the wake word by creating a new `.ppn` file in Picovoice Console
- Modify the slide advancement key in the dropdown

## Limitations

- Requires an internet connection for initial Picovoice setup (needed for account checks. All processing happens offline)
- Performance depends on microphone quality

## License

[MIT](https://choosealicense.com/licenses/mit/)
