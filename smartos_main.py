#!/usr/bin/env python3
"""
SmartOS - Voice/Chat-Based AI Operating System Assistant
Version 1.0
A lightweight AI OS assistant that transforms natural language into executable system tasks.
"""

import os
import sys
import json
import time
import threading
import subprocess
import logging
import speech_recognition as sr
import pyttsx3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse
import traceback

class SmartOSCore:
    """Core SmartOS functionality for natural language processing and system control"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.setup_logging()
        self.voice_engine = None
        self.speech_recognizer = None
        self.command_history = []
        self.execution_metrics = {
            "total_commands": 0,
            "successful_commands": 0,
            "failed_commands": 0,
            "average_response_time": 0.0
        }
        self._initialize_voice_components()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        default_config = {
            "voice_enabled": True,
            "response_timeout": 3.0,
            "log_level": "INFO",
            "supported_apps": [
                "notepad", "calculator", "browser", "explorer", 
                "cmd", "powershell", "code", "word", "excel"
            ],
            "fallback_mode": True,
            "screenshot_on_error": True,
            "background_execution": True
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                
        return default_config
    
    def setup_logging(self):
        """Initialize logging system"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, self.config["log_level"]),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"smartos_{datetime.now().strftime('%Y%m%d')}.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger("SmartOS")
    
    def _initialize_voice_components(self):
        """Initialize voice recognition and TTS components"""
        if not self.config["voice_enabled"]:
            return
            
        try:
            # Initialize TTS engine
            self.voice_engine = pyttsx3.init()
            voices = self.voice_engine.getProperty('voices')
            if voices:
                self.voice_engine.setProperty('voice', voices[0].id)
            self.voice_engine.setProperty('rate', 180)
            
            # Initialize speech recognition
            self.speech_recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with self.microphone as source:
                self.speech_recognizer.adjust_for_ambient_noise(source, duration=1)
                
            self.logger.info("Voice components initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Voice initialization failed: {e}")
            self.config["voice_enabled"] = False

class NLUProcessor:
    """Natural Language Understanding processor for command interpretation"""
    
    def __init__(self, core: SmartOSCore):
        self.core = core
        self.intent_patterns = self._load_intent_patterns()
    
    def _load_intent_patterns(self) -> Dict:
        """Load predefined intent patterns for command recognition"""
        return {
            "open_application": {
                "keywords": ["open", "launch", "start", "run"],
                "apps": {
                    "notepad": ["notepad", "text editor", "note"],
                    "calculator": ["calculator", "calc"],
                    "browser": ["browser", "chrome", "firefox", "edge", "internet"],
                    "explorer": ["explorer", "file manager", "files", "folder"],
                    "cmd": ["command prompt", "cmd", "terminal", "console"],
                    "powershell": ["powershell", "ps"],
                    "code": ["vscode", "visual studio code", "code editor", "vs code"],
                    "word": ["word", "microsoft word", "document"],
                    "excel": ["excel", "spreadsheet", "microsoft excel"]
                }
            },
            "file_operations": {
                "keywords": ["create", "write", "save", "delete", "copy", "move"],
                "actions": {
                    "create": ["create", "make", "new"],
                    "write": ["write", "type", "add content", "insert"],
                    "save": ["save", "store"],
                    "delete": ["delete", "remove", "erase"],
                    "copy": ["copy", "duplicate"],
                    "move": ["move", "transfer", "relocate"]
                }
            },
            "system_control": {
                "keywords": ["shutdown", "restart", "sleep", "hibernate", "lock"],
                "wifi": ["wifi", "wireless", "internet connection", "network"],
                "bluetooth": ["bluetooth", "bt"],
                "volume": ["volume", "sound", "audio"]
            },
            "content_creation": {
                "keywords": ["write essay", "create document", "compose", "draft"],
                "types": ["essay", "document", "letter", "report", "email"]
            }
        }
    
    def parse_command(self, command: str) -> Dict[str, Any]:
        """Parse natural language command into structured intent"""
        command_lower = command.lower().strip()
        
        intent = {
            "action": "unknown",
            "target": "",
            "parameters": {},
            "confidence": 0.0,
            "original_command": command
        }
        
        # Application opening detection
        for keyword in self.intent_patterns["open_application"]["keywords"]:
            if keyword in command_lower:
                intent["action"] = "open_application"
                for app, aliases in self.intent_patterns["open_application"]["apps"].items():
                    if any(alias in command_lower for alias in aliases):
                        intent["target"] = app
                        intent["confidence"] = 0.9
                        break
                break
        
        # File operations detection
        if intent["action"] == "unknown":
            for keyword in self.intent_patterns["file_operations"]["keywords"]:
                if keyword in command_lower:
                    intent["action"] = "file_operation"
                    for action, aliases in self.intent_patterns["file_operations"]["actions"].items():
                        if any(alias in command_lower for alias in aliases):
                            intent["target"] = action
                            intent["confidence"] = 0.8
                            # Extract file name/path if present
                            if "file" in command_lower or "document" in command_lower:
                                words = command.split()
                                for i, word in enumerate(words):
                                    if word.lower() in ["file", "document"] and i + 1 < len(words):
                                        intent["parameters"]["filename"] = words[i + 1]
                                        break
                            break
                    break
        
        # System control detection
        if intent["action"] == "unknown":
            for keyword in self.intent_patterns["system_control"]["keywords"]:
                if keyword in command_lower:
                    intent["action"] = "system_control"
                    intent["target"] = keyword
                    intent["confidence"] = 0.85
                    break
        
        # Content creation detection
        if intent["action"] == "unknown":
            for keyword in self.intent_patterns["content_creation"]["keywords"]:
                if any(k in command_lower for k in keyword.split()):
                    intent["action"] = "content_creation"
                    for content_type in self.intent_patterns["content_creation"]["types"]:
                        if content_type in command_lower:
                            intent["target"] = content_type
                            intent["confidence"] = 0.75
                            # Extract topic if present
                            if "about" in command_lower:
                                topic_start = command_lower.find("about") + 5
                                intent["parameters"]["topic"] = command[topic_start:].strip()
                            break
                    break
        
        return intent

class TaskExecutor:
    """Execute system tasks based on parsed intents"""
    
    def __init__(self, core: SmartOSCore):
        self.core = core
        self.app_commands = self._get_app_commands()
    
    def _get_app_commands(self) -> Dict[str, str]:
        """Platform-specific application launch commands"""
        if sys.platform.startswith('win'):
            return {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "browser": "start chrome",
                "explorer": "explorer.exe",
                "cmd": "cmd.exe",
                "powershell": "powershell.exe",
                "code": "code",
                "word": "winword.exe",
                "excel": "excel.exe"
            }
        elif sys.platform.startswith('darwin'):  # macOS
            return {
                "notepad": "open -a TextEdit",
                "calculator": "open -a Calculator",
                "browser": "open -a Safari",
                "explorer": "open -a Finder",
                "cmd": "open -a Terminal",
                "code": "code",
            }
        else:  # Linux
            return {
                "notepad": "gedit",
                "calculator": "gnome-calculator",
                "browser": "firefox",
                "explorer": "nautilus",
                "cmd": "gnome-terminal",
                "code": "code",
            }
    
    def execute_intent(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the parsed intent and return result"""
        start_time = time.time()
        result = {
            "success": False,
            "message": "",
            "execution_time": 0.0,
            "error": None,
            "screenshot": None
        }
        
        try:
            if intent["action"] == "open_application":
                result = self._execute_app_launch(intent)
            elif intent["action"] == "file_operation":
                result = self._execute_file_operation(intent)
            elif intent["action"] == "system_control":
                result = self._execute_system_control(intent)
            elif intent["action"] == "content_creation":
                result = self._execute_content_creation(intent)
            else:
                result["message"] = f"Unknown command: {intent['original_command']}"
                
            result["execution_time"] = time.time() - start_time
            
        except Exception as e:
            result["error"] = str(e)
            result["execution_time"] = time.time() - start_time
            self.core.logger.error(f"Execution error: {e}")
            
            if self.core.config["screenshot_on_error"]:
                result["screenshot"] = self._capture_screenshot()
        
        return result
    
    def _execute_app_launch(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Launch application based on intent"""
        app_name = intent["target"]
        command = self.app_commands.get(app_name)
        
        if not command:
            return {
                "success": False,
                "message": f"Application '{app_name}' not supported or not found"
            }
        
        try:
            if sys.platform.startswith('win'):
                subprocess.Popen(command, shell=True)
            else:
                subprocess.Popen(command.split())
            
            return {
                "success": True,
                "message": f"Successfully launched {app_name}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to launch {app_name}: {str(e)}"
            }
    
    def _execute_file_operation(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Execute file operations"""
        operation = intent["target"]
        filename = intent["parameters"].get("filename", "untitled.txt")
        
        try:
            if operation == "create":
                Path(filename).touch()
                return {"success": True, "message": f"Created file: {filename}"}
            elif operation == "write":
                content = intent["parameters"].get("content", "Sample content")
                with open(filename, 'w') as f:
                    f.write(content)
                return {"success": True, "message": f"Written content to: {filename}"}
            elif operation == "delete":
                if os.path.exists(filename):
                    os.remove(filename)
                    return {"success": True, "message": f"Deleted file: {filename}"}
                else:
                    return {"success": False, "message": f"File not found: {filename}"}
            else:
                return {"success": False, "message": f"File operation '{operation}' not implemented"}
                
        except Exception as e:
            return {"success": False, "message": f"File operation failed: {str(e)}"}
    
    def _execute_system_control(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Execute system control commands"""
        action = intent["target"]
        
        try:
            if sys.platform.startswith('win'):
                if action == "shutdown":
                    subprocess.run(["shutdown", "/s", "/t", "60"])
                elif action == "restart":
                    subprocess.run(["shutdown", "/r", "/t", "60"])
                elif action == "lock":
                    subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
            else:
                if action == "shutdown":
                    subprocess.run(["sudo", "shutdown", "-h", "+1"])
                elif action == "restart":
                    subprocess.run(["sudo", "shutdown", "-r", "+1"])
                elif action == "lock":
                    subprocess.run(["gnome-screensaver-command", "-l"])
            
            return {"success": True, "message": f"System {action} initiated"}
            
        except Exception as e:
            return {"success": False, "message": f"System control failed: {str(e)}"}
    
    def _execute_content_creation(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Create content based on intent"""
        content_type = intent["target"]
        topic = intent["parameters"].get("topic", "general topic")
        
        # Generate sample content (in a real implementation, this would use AI)
        content_templates = {
            "essay": f"# Essay on {topic}\n\nIntroduction:\n\nBody:\n\nConclusion:",
            "document": f"Document: {topic}\n\nContent goes here...",
            "letter": f"Dear [Recipient],\n\nRegarding: {topic}\n\nSincerely,\n[Your Name]",
            "report": f"# Report: {topic}\n\n## Executive Summary\n\n## Findings\n\n## Recommendations"
        }
        
        content = content_templates.get(content_type, f"Content about {topic}")
        filename = f"{content_type}_{topic.replace(' ', '_')}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(content)
            
            # Optionally open the created file
            if sys.platform.startswith('win'):
                subprocess.Popen(["notepad.exe", filename])
            else:
                subprocess.Popen(["gedit", filename])
            
            return {"success": True, "message": f"Created {content_type} about {topic}: {filename}"}
            
        except Exception as e:
            return {"success": False, "message": f"Content creation failed: {str(e)}"}
    
    def _capture_screenshot(self) -> Optional[str]:
        """Capture screenshot for error logging"""
        try:
            import PIL.ImageGrab as ImageGrab
            screenshot_dir = Path("screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = screenshot_dir / f"error_{timestamp}.png"
            
            screenshot = ImageGrab.grab()
            screenshot.save(screenshot_path)
            
            return str(screenshot_path)
        except Exception:
            return None

class SmartOSInterface:
    """Main interface for SmartOS with voice and text interaction"""
    
    def __init__(self):
        self.core = SmartOSCore()
        self.nlu = NLUProcessor(self.core)
        self.executor = TaskExecutor(self.core)
        self.running = False
        
    def start_voice_loop(self):
        """Start the voice interaction loop"""
        if not self.core.config["voice_enabled"]:
            self.core.logger.warning("Voice not enabled, falling back to text mode")
            return self.start_text_loop()
        
        self.core.logger.info("SmartOS Voice Assistant started. Say 'exit' to quit.")
        self.speak("SmartOS Voice Assistant is ready. How can I help you?")
        
        self.running = True
        while self.running:
            try:
                command = self.listen_for_command()
                if command:
                    if command.lower() in ["exit", "quit", "stop"]:
                        self.speak("Goodbye!")
                        break
                    
                    self.process_command(command)
                    
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                break
            except Exception as e:
                self.core.logger.error(f"Voice loop error: {e}")
                self.speak("Sorry, I encountered an error. Please try again.")
    
    def start_text_loop(self):
        """Start the text-based interaction loop"""
        self.core.logger.info("SmartOS Text Assistant started. Type 'exit' to quit.")
        print("SmartOS Text Assistant is ready. How can I help you?")
        
        self.running = True
        while self.running:
            try:
                command = input("\nSmartOS> ").strip()
                if not command:
                    continue
                    
                if command.lower() in ["exit", "quit", "stop"]:
                    print("Goodbye!")
                    break
                
                self.process_command(command)
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                self.core.logger.error(f"Text loop error: {e}")
                print("Sorry, I encountered an error. Please try again.")
    
    def listen_for_command(self) -> Optional[str]:
        """Listen for voice command"""
        try:
            with self.core.microphone as source:
                print("Listening...")
                audio = self.core.speech_recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("Processing...")
            command = self.core.speech_recognizer.recognize_google(audio)
            print(f"Heard: {command}")
            return command
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except Exception as e:
            self.core.logger.error(f"Speech recognition error: {e}")
            return None
    
    def speak(self, text: str):
        """Text-to-speech output"""
        if self.core.voice_engine:
            self.core.voice_engine.say(text)
            self.core.voice_engine.runAndWait()
        print(f"SmartOS: {text}")
    
    def process_command(self, command: str):
        """Process and execute a command"""
        self.core.logger.info(f"Processing command: {command}")
        
        # Parse the command
        intent = self.nlu.parse_command(command)
        self.core.logger.info(f"Parsed intent: {intent}")
        
        if intent["confidence"] < 0.5:
            response = f"I'm not sure how to handle: '{command}'. Could you rephrase?"
            if self.core.config["voice_enabled"]:
                self.speak(response)
            else:
                print(f"SmartOS: {response}")
            return
        
        # Execute the command
        result = self.executor.execute_intent(intent)
        
        # Update metrics
        self.core.execution_metrics["total_commands"] += 1
        if result["success"]:
            self.core.execution_metrics["successful_commands"] += 1
        else:
            self.core.execution_metrics["failed_commands"] += 1
        
        # Calculate average response time
        total_time = (self.core.execution_metrics["average_response_time"] * 
                     (self.core.execution_metrics["total_commands"] - 1) + 
                     result["execution_time"])
        self.core.execution_metrics["average_response_time"] = total_time / self.core.execution_metrics["total_commands"]
        
        # Log the result
        self.log_execution_result(command, intent, result)
        
        # Provide feedback
        if result["success"]:
            response = result["message"]
        else:
            response = f"Failed to execute command: {result.get('message', 'Unknown error')}"
        
        if self.core.config["voice_enabled"]:
            self.speak(response)
        else:
            print(f"SmartOS: {response}")
    
    def log_execution_result(self, command: str, intent: Dict, result: Dict):
        """Log execution results for evaluation"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "intent": intent,
            "result": result,
            "execution_time": result["execution_time"]
        }
        
        # Save to JSON log
        log_dir = Path("execution_logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"execution_{datetime.now().strftime('%Y%m%d')}.json"
        
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def get_metrics(self) -> Dict:
        """Get current execution metrics"""
        return self.core.execution_metrics.copy()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="SmartOS - AI Operating System Assistant")
    parser.add_argument("--mode", choices=["voice", "text"], default="voice",
                       help="Interaction mode (voice or text)")
    parser.add_argument("--config", default="config.json",
                       help="Configuration file path")
    
    args = parser.parse_args()
    
    try:
        # Initialize SmartOS
        smart_os = SmartOSInterface()
        
        # Start appropriate interface
        if args.mode == "voice":
            smart_os.start_voice_loop()
        else:
            smart_os.start_text_loop()
            
    except Exception as e:
        print(f"Failed to start SmartOS: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
