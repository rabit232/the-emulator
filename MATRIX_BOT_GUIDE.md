# The Emulator Matrix Bot Guide

## Overview

The Emulator Matrix Bot integrates The Emulator's advanced AI capabilities with Matrix.org chat rooms, providing intelligent automation and conversation capabilities with sophisticated user authentication and command restrictions.

## Features

### 🤖 **Advanced AI Integration**
- **AdvancedLLMEmulator** with emotional intelligence
- **50+ emotions** for context-aware responses
- **Multi-language programming support** (10 languages)
- **Sophisticated reasoning** and knowledge management
- **Persistent conversation context** per room

### 🔐 **Security & Authentication**
- **Authorized user system** with specific Matrix user IDs
- **Command-level permissions** for system operations
- **Rate limiting** and abuse protection
- **Terminator mode** responses for unauthorized users

### 💬 **Matrix Integration**
- **Auto-join rooms** when invited
- **Multiple trigger words** (`ribit.2.0`, `emulator`, `ribit`)
- **Conversation context management** per room
- **Graceful error handling** and reconnection
- **Mock mode** for development without Matrix server

## Configuration

### User Handles

The bot is configured for the following Matrix identities:

- **Bot Identity:** `@ribit.2.0:envs.net`
- **Authorized Users:**
  - `@rabit233:matrix.anarchists.space`
  - `@rabit232:envs.net`

### Environment Setup

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your Matrix credentials:**
   ```bash
   MATRIX_HOMESERVER=https://envs.net
   MATRIX_USERNAME=@ribit.2.0:envs.net
   MATRIX_PASSWORD=your_actual_password
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Bot

```bash
# Run the Matrix bot
python run_matrix_bot.py

# Or make it executable and run directly
chmod +x run_matrix_bot.py
./run_matrix_bot.py
```

### Chat Commands

#### **General Chat**
- `ribit.2.0 <message>` - Chat with the AI
- `emulator <message>` - Alternative trigger
- `ribit <message>` - Short trigger
- `!reset` - Clear conversation context

#### **Public Commands**
- `?help` - Show available commands and usage

#### **Authorized Commands** (restricted users only)
- `?sys` - Display system status (CPU, memory, disk)
- `?status` - Show bot status and capabilities
- `?command <action>` - Execute system actions

### Example Interactions

```
User: ribit.2.0 tell me about quantum computing
Bot: What a fascinating question! Let me break this down systematically for you...

User: ?help
Bot: 📚 **The Emulator Commands** [shows full help]

Authorized User: ?sys
Bot: 🖥️ **System Status**
     **CPU:** 15.2%
     **Memory:** 45.8% (3GB / 8GB)
     ...

Authorized User: ?command open ms paint and draw a house
Bot: 🎯 **Action Analysis:** open ms paint and draw a house
     🧠 **AI Response:** [intelligent analysis of the request]
```

## Security Features

### Authorization System

Only the following users can execute system commands:
- `@rabit233:matrix.anarchists.space`
- `@rabit232:envs.net`

### Unauthorized User Responses

1. **First attempt:** "🚫 I can't do this silly thing! Only authorized users can execute system commands."
2. **Second attempt:** "🤖 Action terminated xd exe! You've tried again. Would you like to enable terminator mode? (Just kidding! 😄)"
3. **Subsequent attempts:** Humorous "terminator mode" responses

## Technical Architecture

### Core Components

```
EmulatorMatrixBot
├── AdvancedLLMEmulator (AI engine)
├── EmotionalIntelligence (50+ emotions)
├── MultiLanguageSupport (10 languages)
├── KnowledgeManager (persistent storage)
└── AdvancedSettingsManager (configuration)
```

### Matrix Integration

- **matrix-nio** for Matrix protocol support
- **Async/await** architecture for performance
- **Event-driven** message processing
- **Automatic reconnection** and error recovery
- **Graceful degradation** when Matrix unavailable

### Message Processing Flow

1. **Receive Matrix message**
2. **Check if directed at bot** (trigger words)
3. **Clean message** (remove bot mentions)
4. **Handle commands** or **process as chat**
5. **Generate AI response** using The Emulator
6. **Send response** to Matrix room
7. **Update conversation context**

## Development

### Mock Mode

When Matrix dependencies are unavailable, the bot runs in mock mode:

```bash
python run_matrix_bot.py
# Falls back to console-based simulation
```

### Testing

```bash
# Test core functionality
python examples/basic_usage.py

# Test Matrix bot imports
python -c "from emulator import EmulatorMatrixBot, MATRIX_AVAILABLE; print(f'Matrix: {MATRIX_AVAILABLE}')"
```

### Extending Functionality

The bot is designed for easy extension:

1. **Add new commands** in `_handle_command()` method
2. **Extend AI capabilities** through The Emulator
3. **Add new triggers** in `_is_message_for_bot()` method
4. **Customize responses** in personality configuration

## Deployment

### Production Deployment

1. **Set up Matrix account** for the bot
2. **Configure environment variables**
3. **Install dependencies** in production environment
4. **Run with process manager** (systemd, supervisor, etc.)
5. **Monitor logs** for errors and performance

### Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run_matrix_bot.py"]
```

### Systemd Service

```ini
[Unit]
Description=The Emulator Matrix Bot
After=network.target

[Service]
Type=simple
User=emulator
WorkingDirectory=/opt/the-emulator
ExecStart=/usr/bin/python3 run_matrix_bot.py
Restart=always
RestartSec=10
Environment=MATRIX_PASSWORD=your_password

[Install]
WantedBy=multi-user.target
```

## Troubleshooting

### Common Issues

1. **Login failures:** Check Matrix credentials and homeserver URL
2. **Import errors:** Install missing dependencies with `pip install -r requirements.txt`
3. **Permission denied:** Ensure authorized users are correctly configured
4. **Connection issues:** Check network connectivity to Matrix homeserver

### Debug Mode

Enable debug logging by setting:
```bash
export EMULATOR_LOG_LEVEL=DEBUG
```

### Logs

The bot provides comprehensive logging:
- **INFO:** Normal operations and status updates
- **WARNING:** Non-critical issues and fallbacks
- **ERROR:** Critical errors requiring attention
- **DEBUG:** Detailed execution information

## Advanced Configuration

### Settings Management

The bot uses `AdvancedSettingsManager` for configuration:

```python
from emulator import AdvancedSettingsManager

settings = AdvancedSettingsManager()
settings.set_setting("matrix.sync_timeout", 60000)
settings.add_authorized_user("@newuser:matrix.org")
```

### Personality Customization

Available personalities:
- `curious_researcher` (default)
- `creative_assistant`
- `wise_mentor`

### Performance Tuning

Key settings for performance optimization:
- `matrix.sync_timeout` - How long to wait for events
- `matrix.keepalive_interval` - Keepalive frequency
- `emulator.max_context_length` - Conversation memory
- `emulator.response_timeout` - AI response timeout

## Support

For issues and questions:
1. Check the logs for error messages
2. Verify Matrix credentials and connectivity
3. Test in mock mode for debugging
4. Review the configuration settings

The Emulator Matrix Bot provides a sophisticated, secure, and extensible platform for AI-powered Matrix automation with the specified user authentication and command system.
