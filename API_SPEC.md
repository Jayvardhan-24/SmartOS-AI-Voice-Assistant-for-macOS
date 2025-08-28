# SmartOS API Specification

## REST Endpoints (Future)

- `POST /api/command` → Execute a natural language command
- `GET /api/status` → Retrieve system/assistant status
- `GET /api/metrics` → Get performance metrics
- `POST /api/config` → Update configuration

## JSON Command Schema

```json
{
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

## Plugin Interface

```python
class SmartOSPlugin:
    def execute(self, intent: dict) -> dict:
        pass

    def get_supported_intents(self) -> list:
        pass
```
