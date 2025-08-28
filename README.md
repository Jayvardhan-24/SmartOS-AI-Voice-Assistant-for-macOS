SmartOS – AI Voice Assistant for macOS

SmartOS is an intelligent voice assistant built with Python that helps you control your Mac, perform web searches, open apps, and execute system-level operations using voice commands.
The project works seamlessly on macOS and provides an extendable framework to add new commands.

📌 Features

✅ Voice Recognition – Uses speech-to-text to capture commands.
✅ Text-to-Speech – Speaks responses naturally.
✅ macOS System Control – Shutdown, Restart, Sleep, Lock your Mac.
✅ Application Launcher – Open Chrome, Safari, VS Code, Finder, Terminal, Word, Excel, etc.
✅ Web Search – Perform Google searches with voice.
✅ Websites Access – Open YouTube, Google, GitHub with one command.
✅ Time & Date – Get current system time and date.
✅ Modular Design – Easily extendable for new apps & commands.
✅ Cross-Platform Ready – Current implementation for macOS; Windows/Linux can be added.

🛠️ Tech Stack

Python 3.9+

SpeechRecognition
 – For speech-to-text

pyttsx3
 – For text-to-speech

webbrowser
 – Open websites

macOS System Commands via osascript

📂 Project Structure
SmartOS/
│── smartos_main.py      # Main script with voice assistant logic
│── smartos_ui.py        # Streamlit-based UI (optional extension)
│── requirements.txt     # Python dependencies
│── README.md            # Documentation

⚙️ Installation

Clone the Repository

git clone https://github.com/your-username/SmartOS.git
cd SmartOS


Create Virtual Environment (recommended)

python3 -m venv venv
source venv/bin/activate   # for macOS/Linux


Install Dependencies

pip install -r requirements.txt


Run the Assistant

python smartos_main.py

🎤 Commands You Can Use
👋 Greetings

Hello → “Hello! How can I help you today?”

⏰ Time & Date

What’s the time → Speaks current time.

What’s the date → Speaks today’s date.

🌐 Web Search

Search → Asks for a topic, then searches on Google.

💻 Open Apps (macOS)

Open Text Editor → Opens TextEdit

Open Calculator → Opens Calculator

Open Chrome / Open Safari → Opens browsers

Open Finder → Opens Finder

Open Terminal → Opens Terminal

Open VS Code → Opens Visual Studio Code

Open Word / Open Excel → Opens Microsoft Office apps (if installed)

🌍 Websites

Open YouTube

Open Google

Open GitHub

🖥️ System Controls

Shutdown → Shuts down your Mac

Restart → Restarts your Mac

Sleep → Puts Mac to sleep

Lock → Locks the screen

🚪 Exit

Exit / Quit / Stop → Closes the assistant
