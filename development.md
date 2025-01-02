# AI Voice Assistant Development Log
Last Updated: 2025-01-01

## Project Overview
Building an AI assistant that monitors emails and provides voice interaction, focusing on:
- Email monitoring with AOL-style notifications
- Priority-based email alerts
- Natural voice interaction

## Component Guide
### Implemented Features
- **Wake Word Detection** (`src/voice/listener.py`)
  - "Hey Q" detection using Porcupine
  - Handles wake word activation
  - Currently working with good accuracy

- **Natural Language Processing** (`src/voice/speech.py`)
  - Uses Whisper for accurate speech-to-text
  - OpenAI Echo for natural conversation
  - Understands context and intent
  - No predefined keywords needed

### In Progress
- **Agent Orchestrator** (`src/orchestrator.py`)
  - Coordinates all agent interactions
  - Manages conversation flow
  - Maintains conversation context
  - Routes intents to appropriate agents

- **Email Agent** (`src/agents/email_agent/email_agent.py`)
  - Monitors Gmail inbox
  - Plays "You've got mail!" notification
  - Natural email discussions
  - Understands email-related queries

### Email Notification Levels
1. **Priority Contacts**
   - "You've got mail!" + automatic follow-up
   - Orchestrator offers to read immediately
   - No wake word needed for interaction

2. **Regular Emails**
   - "You've got mail!" notification only
   - Requires "Hey Q" to check details
   - Must be in primary inbox

3. **Filtered Emails**
   - No notification
   - Still accessible in email summaries
   - Configurable through filters.json

## Project Structure

### Root Directory
```
AI_Assistant/
├── credentials.json             # API keys and secrets
├── Hey-Q.ppn                   # Wake word model file
├── requirements.txt            # Python dependencies
├── .gitignore                  # Version control rules
├── development.md              # Project documentation
└── logs/
    └── app.log                 # Application logs
```

### Source Code
```
AI_Assistant/src/
├── orchestrator.py             # Main coordinator
└── agents/
    ├── email_agent/
    │   ├── email_agent.py      # Email monitoring
    │   ├── settings.json       # Email preferences
    │   ├── filters.json        # Sender rules
    │   └── sounds/
    │       └── youve_got_mail.wav
    └── voice/
        ├── listener.py         # Wake word detection
        ├── speaker.py          # Voice responses
        └── settings.json       # Voice preferences
```

## Key Files Explained

### Root Level
- `credentials.json` - Secure storage for:
  - Gmail API credentials
  - OpenAI API keys
  - Porcupine access key

- `Hey-Q.ppn` - Wake word model:
  - Trained for "Hey Q" detection
  - Used by voice/listener.py
  - Core to wake word system

- `requirements.txt` - Project dependencies:
  - OpenAI libraries
  - Gmail API client
  - Voice processing tools

### Source Code
- `src/orchestrator.py`:
  - Coordinates between agents
  - Manages conversation flow
  - Handles priority interrupts
  - Routes commands to agents

- `src/agents/email_agent/`:
  - `email_agent.py` - Core email functions:
    - Gmail monitoring
    - Email classification
    - Natural language processing
  - `settings.json` - Email preferences:
    - Quiet hours
    - Check frequency
    - Notification settings
  - `filters.json` - Email filtering:
    - Priority senders list
    - Ignore rules
  - `sounds/youve_got_mail.wav` - AOL notification

- `src/voice/`:
  - `listener.py` - Audio input:
    - Wake word detection (local via Porcupine)
    - Stream processing with sounddevice
    - Whisper speech-to-text (local model)
    - Audio buffering and cleanup
  - `speaker.py` - Audio output:
    - Text-to-speech via pyttsx3 (local)
    - Sound file playback
    - Audio device management
  - `settings.json` - Voice settings:
    - Whisper model selection (tiny, base, small)
    - Wake word sensitivity
    - Audio device selection
    - Buffer sizes and timeouts

### Processing Methods
#### Local Processing
- Wake word detection (Porcupine)
- Speech-to-text (Whisper local model)
- Text-to-speech (pyttsx3)
- Audio streaming (sounddevice)
- Sound playback (local wav files)

#### API Services
- OpenAI Echo for natural language understanding
- Gmail API for email monitoring
- Future API integrations

### System Files
- `logs/app.log` - System logging:
  - Error tracking
  - Debug information
  - Activity history

- `.gitignore` - Excludes from git:
  - Private credentials
  - Cache files
  - Logs

## Development Guidelines
### Code Style
- Maximum function length: 20 lines
- Type hints required
- Document all public functions
- Unit tests for core features

### Memory Management
- Stream audio processing
- Batch email operations
- Regular cache cleanup

## Development Workflow

### Environment Management
- Standard Python virtual environment (.venv)
- All commands run by user (not AI)
- Environment setup:
  ```bash
  # Initial setup (run by user)
  python -m venv .venv
  .venv\Scripts\activate
  pip install -r requirements.txt
  ```

### Code Style Preferences
- Small, focused functions
- Clear commenting style:
  ```python
  def process_email(email: Email) -> bool:
      # Check if email is from priority sender
      if email.sender in priority_list:
          return handle_priority_email(email)

      # Skip automated notifications
      if is_automated(email):
          return False

      return handle_regular_email(email)
  ```

### Development Process Guidelines for working with AI
1. **Small Steps**
   - Work on one feature at a time
   - Test each component before moving on
   - Commit working code frequently

2. **AI Interaction**
   - Discuss implementation details first
   - AI suggests code structure
   - User handles all command execution
   - Minimal token usage in discussions

3. **Testing Approach**
   - Test each component in isolation
   - Manual testing by user
   - Fix issues before moving forward

4. **Resource Management**
   - Careful API token usage
   - Local processing when possible
   - User controls all external services

### Common Commands
```bash
# Always run by user, never by AI
pip install package-name   # Add new dependency
pip freeze > requirements.txt  # Update dependencies
python src/orchestrator.py    # Run main program
```

## Example Workflow
### Priority Email
```
1. Email arrives from priority sender
EmailAgent: *plays "You've got mail!"*
Orchestrator: "That email was from an important contact. Would you like me to read it?"
YOU: "Yeah, but first tell me what it's about"
Orchestrator: "It's about tomorrow's project deadline. The subject is 'Updated Timeline'"
YOU: "Okay go ahead and read it"
Orchestrator: *reads email content*
YOU: "Can you draft a quick response saying I'll review it tonight?"
Orchestrator: *drafts and shows response*
```

### Regular Email
```
1. Email arrives in primary inbox
EmailAgent: *plays "You've got mail!"*
YOU: "Hey Q"
Orchestrator: "Listening..."
YOU: "What's the new email that just arrived?"
      or
YOU: "who just emailed me?"
Orchestrator: "You got an email from Sarah about the team lunch"
YOU: "What's she saying?"
Orchestrator: *reads email naturally*
YOU: "Cool, remind me to respond in an hour"
Orchestrator: "Sure, I'll remind you about Sarah's email in an hour"
```

### Error Handling Scenarios
# Wake Word Detection Issue
YOU: "Hey Q" (in noisy environment)
Orchestrator: *no response*
YOU: "Hey Q" (speaking clearer)
Orchestrator: "Listening..."

# Email Connection Lost
EmailAgent: *detects connection issue*
Orchestrator: "I've lost connection to your email. I'll keep trying and let you know when it's back."
*connection restored*
Orchestrator: "Email connection restored. You have 3 new messages while we were offline."

# Unclear Speech
YOU: "Hey Q"
Orchestrator: "Listening..."
YOU: *mumbled speech*
Orchestrator: "I didn't catch that. Could you say it again?"
YOU: "Who emailed me last?"
Orchestrator: "The last email was from..."

# Email Access Error
EmailAgent: *Gmail API token expired*
Orchestrator: "I'm having trouble accessing your emails. You might need to re-authenticate. Would you like me to guide you through that?"
YOU: "Yes please"
Orchestrator: *starts authentication process*

## Implementation Examples
### Email Agent Settings (settings.json)
```python
{
    "quiet_hours": {
        "enabled": true,
        "start_time": "22:00",
        "end_time": "07:00"
    },
    "notifications": {
        "sound_enabled": true,
        "check_frequency": "30s"
    }
}
```

### Email Filtering Rules (filters.json)
```python
{
    "priority_senders": [
        "boss@company.com",
        "important@client.com"
    ],
    "ignore_list": [
        "noreply@automated.com",
        "notifications@system.com"
    ]
}
```

### Voice Settings (voice/settings.json)
```python
{
    "speech": {
        "volume": 0.8,
        "speed": 1.0,
        "language": "en-US"
    },
    "wake_word": {
        "sensitivity": 0.5,
        "timeout": "5s"
    }
}
```
