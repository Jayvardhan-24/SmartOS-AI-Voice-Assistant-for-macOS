# SmartOS - AI Operating System Assistant

## Version 1.0 - Installation Guide & User Manual

### Overview

SmartOS is a lightweight AI Operating System Assistant that transforms natural language (text or voice) into executable system tasks. It serves as a "local ChatGPT meets Windows Spotlight meets AutoGPT" solution, enabling users to control and operate desktop systems using plain English commands.

## Features

- **Voice & Text Command Processing**: Natural language understanding for system control
- **Desktop Automation**: Execute system-level actions (open apps, manage files, system control)
- **Content Creation**: Automated document creation and editing
- **Multi-modal Interaction**: Support for both voice and text input
- **Comprehensive Logging**: Detailed execution tracking and performance metrics
- **Cross-platform Support**: Windows, macOS, and Linux compatibility
- **Docker Deployment**: Containerized deployment option
- **Extensive Testing**: 50 test cases across 3 difficulty tiers

## System Requirements

### Minimum Requirements
- Python 3.8 or higher
- 2GB RAM
- 1GB free disk space
- Audio input/output devices (for voice features)

### Recommended Requirements
- Python 3.9 or higher
- 4GB RAM
- 2GB free disk space
- High-quality microphone and speakers
- Modern multi-core processor

### Supported Platforms
- Windows 10/11
- macOS 10.14 or higher
- Ubuntu 18.04 or higher
- Other Linux distributions (with package manager support)

## Installation

### Option 1: Direct Python Installation

1. **Clone or download the SmartOS files:**
   ```bash
   # Download all SmartOS files to a directory
   mkdir smartos
   cd smartos
   # Copy smartos_main.py, config.json, requirements.txt to this directory
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Platform-specific audio dependencies:**

   **Windows:**
   ```bash
   # Audio dependencies usually come with Python
   # If issues occur, install: pip install pipwin && pipwin install pyaudio
   ```

   **macOS:**
   ```bash
   brew install portaudio
   pip install pyaudio
   ```

   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt-get update
   sudo apt-get install portaudio19-dev python3-pyaudio espeak espeak-data
   ```

4. **Verify installation:**
   ```bash
   python smartos_main.py --mode text
   ```

### Option 2: Docker Deployment

1. **Build Docker image:**
   ```bash
   docker build -t smartos:1.0 .
   ```

2. **Run SmartOS in container:**
   ```bash
   # Text mode
   docker run -it smartos:1.0

   # With voice support (Linux hosts)
   docker run -it --device /dev/snd smartos:1.0 ./start_smartos.sh --mode voice
   ```

3. **Run with volume mounting for persistent data:**
   ```bash
   docker run -it -v $(pwd)/data:/app/data smartos:1.0
   ```

## Configuration

### config.json Parameters

```json
{
  "voice_enabled": true,              // Enable/disable voice features
  "response_timeout": 3.0,           // Maximum response time in seconds
  "log_level": "INFO",               // Logging level (DEBUG, INFO, WARNING, ERROR)
  "supported_apps": [...],           // List of supported applications
  "fallback_mode": true,             // Enable fallback to text mode
  "screenshot_on_error": true,       // Capture screenshots on errors
  "background_execution": true       // Allow background task execution
}
```

### Security Settings

```json
{
  "security_settings": {
    "require_confirmation": false,     // Require user confirmation for system commands
    "allowed_directories": [...],     // Restrict file operations to specific directories
    "blocked_commands": [...]         // List of blocked dangerous commands
  }
}
```

## Usage Guide

### Starting SmartOS

#### Text Mode (Recommended for first use)
```bash
python smartos_main.py --mode text
```

#### Voice Mode
```bash
python smartos_main.py --mode voice
```

#### Custom Configuration
```bash
python smartos_main.py --mode text --config custom_config.json
```

### Command Examples

#### Application Control
- "Open notepad"
- "Launch calculator"
- "Start browser"
- "Open file explorer"
- "Run command prompt"

#### File Operations
- "Create file report.txt"
- "Write content to document.txt"
- "Delete file old_data.txt"
- "Copy file backup.txt"

#### Content Creation
- "Write essay about technology"
- "Create document about artificial intelligence"
- "Compose letter about job application"
- "Draft report about climate change"

#### System Control
- "Lock the system"
- "Restart computer"
- "Shutdown in 5 minutes"

### Voice Commands

1. **Start voice mode**
2. **Wait for "Listening..." prompt**
3. **speak clearly and naturally**
4. **Wait for processing and response**
5. **Say "exit" to quit**

### Text Commands

1. **Type commands at the SmartOS> prompt**
2. **Press Enter to execute**
3. **Type "exit" to quit**

## API Specification

### Command Processing Flow

```python
# Input: Natural language command
command = "open notepad"

# Step 1: Parse command into intent
intent = {
    "action": "open_application",
    "target": "notepad", 
    "parameters": {},
    "confidence": 0.9
}

# Step 2: Execute intent
result = {
    "success": True,
    "message": "Successfully launched notepad",
    "execution_time": 1.23,
    "error": None,
    "screenshot": None
}
```

### JSON Output Format

```json
{
  "timestamp": "2025-08-28T10:30:00",
  "command": "open calculator",
  "intent": {
    "action": "open_application",
    "target": "calculator",
    "confidence": 0.9
  },
  "result": {
    "success": true,
    "message": "Successfully launched calculator",
    "execution_time": 0.85
  }
}
```

## Testing

### Running the Test Suite

```bash
python smartos_test_suite.py
```

### Test Categories

- **Tier 1 (Easy)**: 20 tests - Simple application launches
- **Tier 2 (Medium)**: 20 tests - Multi-step operations
- **Tier 3 (Hard)**: 10 tests - Complex workflows

### Success Criteria

- Pass rate >90% on evaluation dataset
- Response time <3 seconds for 80% of tasks  
- Full autonomous task execution without manual correction

### Evaluation Metrics

1. **Accuracy**: Manual validation of execution correctness
2. **Latency**: Time to execute task
3. **Robustness**: Recovery from bad inputs
4. **Performance**: Benchmarking across task categories

## Troubleshooting

### Common Issues

#### Voice Recognition Not Working
```bash
# Check microphone permissions
# Windows: Settings > Privacy > Microphone
# macOS: System Preferences > Security & Privacy > Microphone
# Linux: Check PulseAudio configuration
```

#### Application Launch Failures
```bash
# Verify application paths in config
# Check system PATH environment variable
# Ensure applications are installed and accessible
```

#### Permission Errors
```bash
# Run with appropriate permissions
# Windows: Run as Administrator if needed
# Linux/macOS: Check file permissions and sudo access
```

### Debug Mode

```bash
# Enable debug logging
python smartos_main.py --mode text --config debug_config.json
```

Create debug_config.json:
```json
{
  "log_level": "DEBUG",
  "voice_enabled": false,
  "screenshot_on_error": true
}
```

### Log Files

- **Application logs**: `logs/smartos_YYYYMMDD.log`
- **Execution logs**: `execution_logs/execution_YYYYMMDD.json`
- **Test results**: `test_results/smartos_test_results_TIMESTAMP.json`

## Advanced Configuration

### Adding Custom Applications

```json
{
  "supported_apps": [
    "custom_app"
  ],
  "custom_commands": {
    "custom_app": {
      "windows": "C:\\Program Files\\CustomApp\\app.exe",
      "macos": "/Applications/CustomApp.app",
      "linux": "custom-app"
    }
  }
}
```

### Extending Command Patterns

```python
# Add to NLUProcessor._load_intent_patterns()
"custom_intent": {
    "keywords": ["custom", "special"],
    "actions": {
        "custom_action": ["do something", "perform task"]
    }
}
```

## API Integration

### REST API (Future Enhancement)

```python
# Planned REST endpoints
POST /api/command
GET /api/status
GET /api/metrics
POST /api/config
```

### Plugin System (Future Enhancement)

```python
# Plugin interface
class SmartOSPlugin:
    def execute(self, intent: Dict) -> Dict:
        pass
    
    def get_supported_intents(self) -> List[str]:
        pass
```

## Performance Optimization

### Memory Usage
- Monitor with `memory_profiler`
- Optimize intent processing
- Cache frequently used commands

### Response Time
- Profile with `line_profiler`
- Optimize system calls
- Implement command prediction

### Accuracy Improvements
- Expand intent patterns
- Add context awareness
- Implement learning from corrections

## Security Considerations

### Command Restrictions
- Whitelist safe applications
- Block dangerous system commands
- Implement confirmation for destructive actions

### File System Access
- Restrict to user directories
- Validate file paths
- Prevent path traversal attacks

### Network Security
- No network access by default
- Secure API endpoints if enabled
- Encrypt sensitive configurations

## Deployment Guide

### Production Deployment

1. **Environment Setup**
   ```bash
   # Create production environment
   python -m venv smartos_prod
   source smartos_prod/bin/activate
   pip install -r requirements.txt
   ```

2. **Configuration**
   ```json
   {
     "log_level": "WARNING",
     "screenshot_on_error": false,
     "require_confirmation": true
   }
   ```

3. **Service Setup (Linux)**
   ```ini
   # /etc/systemd/system/smartos.service
   [Unit]
   Description=SmartOS AI Assistant
   After=network.target

   [Service]
   Type=simple
   User=smartos
   WorkingDirectory=/opt/smartos
   ExecStart=/opt/smartos/venv/bin/python smartos_main.py --mode text
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```

### Scaling Considerations

- Multiple instances for different users
- Load balancing for API mode
- Database backend for command history
- Monitoring and alerting integration

## Support and Maintenance

### Regular Maintenance
- Update dependencies regularly
- Monitor log files for errors
- Review and update intent patterns
- Performance monitoring and optimization

### Getting Help
- Check log files first
- Review this documentation
- Test with simple commands
- Contact support with detailed error information

### Contributing
- Follow code style guidelines
- Add comprehensive tests
- Update documentation