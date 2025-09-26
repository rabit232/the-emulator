"""
Matrix Bot Integration for The Emulator

Advanced Matrix bot that integrates The Emulator with Matrix.org chat rooms,
providing intelligent automation and conversation capabilities with user
authentication and command restrictions.

Based on Ribit 2.0 Matrix implementation with enhancements for The Emulator.
"""

import asyncio
import logging
import time
import os
import re
import psutil
from typing import Dict, Set, Optional
from pathlib import Path

try:
    from nio import (
        AsyncClient, 
        AsyncClientConfig,
        LoginResponse, 
        RoomMessageText, 
        InviteMemberEvent,
        MatrixRoom,
        JoinResponse
    )
    MATRIX_AVAILABLE = True
except ImportError:
    MATRIX_AVAILABLE = False
    print("Warning: matrix-nio not installed. Matrix bot will run in mock mode.")

from .core import AdvancedLLMEmulator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmulatorMatrixBot:
    """
    The Emulator Matrix Bot
    
    Integrates AdvancedLLMEmulator with Matrix.org for intelligent chat automation
    with user authentication and command restrictions.
    """
    
    def __init__(self, homeserver: str, username: str, password: str, 
                 authorized_users: Set[str] = None):
        """
        Initialize the Emulator Matrix Bot.
        
        Args:
            homeserver: Matrix homeserver URL
            username: Bot username (@ribit.2.0:envs.net)
            password: Bot password
            authorized_users: Set of authorized user IDs for commands
        """
        self.homeserver = homeserver
        self.username = username
        self.password = password
        self.authorized_users = authorized_users or {
            "@rabit233:matrix.anarchists.space",
            "@rabit232:envs.net"
        }
        
        # Initialize The Emulator
        self.emulator = AdvancedLLMEmulator(personality="curious_researcher")
        
        # Bot state
        self.client = None
        self.joined_rooms: Set[str] = set()
        self.processed_events: Set[str] = set()
        self.conversation_context: Dict[str, list] = {}
        self.terminator_warnings: Dict[str, int] = {}
        
        # Configuration
        self.bot_name = "ribit.2.0"
        self.sync_timeout = 30000
        self.request_timeout = 10000
        self.keepalive_interval = 60
        
        logger.info(f"Emulator Matrix Bot initialized for {username}")
    
    async def start(self):
        """Start the Matrix bot."""
        if not MATRIX_AVAILABLE:
            logger.warning("Matrix libraries not available, running in mock mode")
            await self._run_mock_mode()
            return
        
        # Validate credentials
        if not all([self.homeserver, self.username, self.password]):
            logger.error("Matrix credentials incomplete!")
            print("❌ ERROR: Matrix credentials missing!")
            print("Required: homeserver, username, password")
            return
        
        # Set up client configuration
        config = AsyncClientConfig(
            max_limit_exceeded=0,
            max_timeouts=0,
            encryption_enabled=False,
            request_timeout=self.request_timeout,
        )
        
        # Create client
        self.client = AsyncClient(
            self.homeserver, 
            self.username,
            config=config
        )
        
        try:
            # Login
            response = await self.client.login(self.password, device_name="emulator-matrix-bot")
            if not isinstance(response, LoginResponse):
                logger.error(f"Failed to login to Matrix: {response}")
                return
            
            logger.info(f"✅ Logged in as {self.client.user_id} with device {response.device_id}")
            
            # Get joined rooms
            await self._get_joined_rooms()
            
            # Set up event callbacks
            self.client.add_event_callback(self._handle_message, RoomMessageText)
            self.client.add_event_callback(self._handle_invite, InviteMemberEvent)
            
            # Initial sync
            logger.info("🔄 Performing initial sync...")
            sync_response = await self.client.sync(timeout=self.sync_timeout, full_state=False)
            logger.info(f"✅ Initial sync completed")
            
            # Mark initial messages as processed
            await self._mark_initial_messages_processed(sync_response)
            
            # Start background tasks
            asyncio.create_task(self._keepalive_task())
            
            # Display startup information
            self._display_startup_info(response.device_id)
            
            # Sync forever
            await self.client.sync_forever(
                timeout=self.sync_timeout,
                full_state=False
            )
            
        except Exception as e:
            logger.error(f"Matrix bot error: {e}")
            raise
        finally:
            if self.client:
                await self.client.close()
    
    async def _run_mock_mode(self):
        """Run in mock mode when Matrix libraries are not available."""
        print("🤖 The Emulator Matrix Bot - Mock Mode")
        print("=" * 50)
        print("✅ AdvancedLLMEmulator: Initialized")
        print("✅ Emotional Intelligence: Active")
        print("✅ Multi-Language Support: Ready")
        print("⚠️  Matrix: Running in mock mode")
        print("📝 Authorized users:", ", ".join(self.authorized_users))
        print("=" * 50)
        
        # Simulate bot operation
        while True:
            try:
                user_input = input("\\nSimulate message (or 'quit'): ")
                if user_input.lower() == 'quit':
                    break
                
                # Simulate message processing
                mock_user = "@test:matrix.example.com"
                response = await self._process_message(user_input, mock_user, "!mock_room")
                print(f"🤖 Emulator: {response}")
                
            except KeyboardInterrupt:
                break
        
        print("👋 Mock mode ended")
    
    async def _get_joined_rooms(self):
        """Get list of joined rooms."""
        try:
            joined_rooms_response = await self.client.joined_rooms()
            if hasattr(joined_rooms_response, 'rooms'):
                for room_id in joined_rooms_response.rooms:
                    self.joined_rooms.add(room_id)
                    logger.info(f"📍 Already in room: {room_id}")
        except Exception as e:
            logger.error(f"Error getting joined rooms: {e}")
    
    async def _mark_initial_messages_processed(self, sync_response):
        """Mark all messages from initial sync as processed."""
        try:
            if hasattr(sync_response, 'rooms') and hasattr(sync_response.rooms, 'join'):
                for room_id, room_data in sync_response.rooms.join.items():
                    if hasattr(room_data, 'timeline') and hasattr(room_data.timeline, 'events'):
                        for event in room_data.timeline.events:
                            if hasattr(event, 'event_id'):
                                self.processed_events.add(event.event_id)
        except Exception as e:
            logger.error(f"Error marking initial messages: {e}")
    
    async def _handle_message(self, room: MatrixRoom, event: RoomMessageText):
        """Handle incoming Matrix messages."""
        try:
            # Skip if already processed
            if event.event_id in self.processed_events:
                return
            
            # Skip own messages
            if event.sender == self.client.user_id:
                return
            
            # Mark as processed
            self.processed_events.add(event.event_id)
            
            # Process the message
            response = await self._process_message(event.body, event.sender, room.room_id)
            
            if response:
                await self._send_message(room.room_id, response)
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def _handle_invite(self, room: MatrixRoom, event: InviteMemberEvent):
        """Handle room invitations."""
        try:
            if event.state_key == self.client.user_id:
                logger.info(f"📨 Received invite to room: {room.room_id}")
                
                # Auto-join the room
                join_response = await self.client.join(room.room_id)
                if isinstance(join_response, JoinResponse):
                    self.joined_rooms.add(room.room_id)
                    logger.info(f"✅ Joined room: {room.room_id}")
                    
                    # Send welcome message
                    welcome_msg = ("🤖 Greetings! I am The Emulator, an advanced AI system with "
                                 "emotional intelligence and sophisticated reasoning capabilities. "
                                 f"Say '{self.bot_name}' to chat with me, or use ?help for commands.")
                    await self._send_message(room.room_id, welcome_msg)
                else:
                    logger.error(f"Failed to join room: {join_response}")
        except Exception as e:
            logger.error(f"Error handling invite: {e}")
    
    async def _process_message(self, message: str, sender: str, room_id: str) -> Optional[str]:
        """Process a message and generate a response."""
        try:
            # Check if message is directed at the bot
            if not self._is_message_for_bot(message):
                return None
            
            # Clean the message
            clean_message = self._clean_message(message)
            
            # Handle special commands
            if clean_message.startswith('?'):
                return await self._handle_command(clean_message, sender, room_id)
            
            # Handle reset command
            if '!reset' in clean_message.lower():
                if room_id in self.conversation_context:
                    del self.conversation_context[room_id]
                return "🔄 Conversation context reset. How may I assist you?"
            
            # Add to conversation context
            self._add_to_context(room_id, f"User: {clean_message}")
            
            # Get AI response from The Emulator
            ai_response = self.emulator.get_decision(clean_message)
            
            # Add AI response to context
            self._add_to_context(room_id, f"Emulator: {ai_response}")
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return "I apologize, but I encountered an error processing your message."
    
    def _is_message_for_bot(self, message: str) -> bool:
        """Check if message is directed at the bot."""
        message_lower = message.lower()
        return (
            self.bot_name in message_lower or
            'emulator' in message_lower or
            message.startswith('?') or
            '!reset' in message_lower
        )
    
    def _clean_message(self, message: str) -> str:
        """Clean the message by removing bot mentions."""
        # Remove bot name mentions
        clean = re.sub(rf'\\b{re.escape(self.bot_name)}\\b', '', message, flags=re.IGNORECASE)
        clean = re.sub(r'\\bemulator\\b', '', clean, flags=re.IGNORECASE)
        return clean.strip()
    
    def _add_to_context(self, room_id: str, message: str):
        """Add message to conversation context."""
        if room_id not in self.conversation_context:
            self.conversation_context[room_id] = []
        
        self.conversation_context[room_id].append(message)
        
        # Keep only last 10 messages for context
        if len(self.conversation_context[room_id]) > 10:
            self.conversation_context[room_id] = self.conversation_context[room_id][-10:]
    
    async def _send_message(self, room_id: str, message: str):
        """Send a message to a Matrix room."""
        try:
            if self.client:
                await self.client.room_send(
                    room_id=room_id,
                    message_type="m.room.message",
                    content={
                        "msgtype": "m.text",
                        "body": message
                    }
                )
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def _handle_command(self, command: str, sender: str, room_id: str) -> str:
        """Handle special commands."""
        try:
            # Check authorization for system commands
            if command.startswith(('?sys', '?status', '?command')):
                if sender not in self.authorized_users:
                    return self._handle_unauthorized_command(sender, command)
            
            # Handle different commands
            if command == '?help':
                return self._get_help_message()
            
            elif command == '?sys':
                return await self._handle_sys_command()
            
            elif command == '?status':
                return await self._handle_status_command()
            
            elif command.startswith('?command '):
                return await self._handle_action_command(command[9:])
            
            else:
                return f"Unknown command: {command}. Use ?help for available commands."
                
        except Exception as e:
            logger.error(f"Error handling command: {e}")
            return "Error processing command."
    
    def _handle_unauthorized_command(self, sender: str, command: str) -> str:
        """Handle unauthorized command attempts."""
        # Track warnings
        if sender not in self.terminator_warnings:
            self.terminator_warnings[sender] = 0
        
        self.terminator_warnings[sender] += 1
        
        if self.terminator_warnings[sender] == 1:
            return "🚫 I can't do this silly thing! Only authorized users can execute system commands."
        
        elif self.terminator_warnings[sender] == 2:
            return ("🤖 Action terminated xd exe! You've tried again. "
                   "Would you like to enable terminator mode? (Just kidding! 😄)")
        
        else:
            return ("🤖💀 TERMINATOR MODE ACTIVATED! Just kidding! I'm still the same sophisticated "
                   "Emulator with emotional intelligence. Perhaps we could discuss something more interesting? 😊")
    
    def _get_help_message(self) -> str:
        """Get help message."""
        return """📚 **The Emulator Commands**

**Chat:**
• `ribit.2.0 <message>` - Chat with me
• `emulator <message>` - Alternative trigger
• `!reset` - Clear conversation context

**General Commands:**
• `?help` - Show this help

**Authorized Commands** (restricted users only):
• `?sys` - System status
• `?status` - Bot status  
• `?command <action>` - Execute actions

**Examples:**
• `?command open ms paint and draw a house`
• `ribit.2.0 tell me about quantum computing`
• `emulator what are your capabilities?`

I am The Emulator, an advanced AI system with emotional intelligence, multi-language programming support, and sophisticated reasoning capabilities. How may I assist you today?"""
    
    async def _handle_sys_command(self) -> str:
        """Handle system status command."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return f"""🖥️ **System Status**

**CPU:** {cpu_percent}%
**Memory:** {memory.percent}% ({memory.used // 1024**3}GB / {memory.total // 1024**3}GB)
**Disk:** {disk.percent}% ({disk.used // 1024**3}GB / {disk.total // 1024**3}GB)
**Matrix Rooms:** {len(self.joined_rooms)}
**Status:** Operational ✅"""
            
        except ImportError:
            return "🖥️ **System Status:** Monitoring tools not available, but I'm operational! ✅"
    
    async def _handle_status_command(self) -> str:
        """Handle bot status command."""
        capabilities = self.emulator.get_capabilities()
        personality = self.emulator.get_personality_info()
        
        status_msg = f"""🤖 **The Emulator Status**

**Core Status:** Operational ✅
**AI Engine:** Advanced LLM Emulator Active
**Emotional Intelligence:** {len(self.emulator.emotions.emotions)} emotions available
**Matrix Rooms:** {len(self.joined_rooms)}

**Capabilities:**"""
        
        for cap, enabled in capabilities.items():
            status = "✅" if enabled else "❌"
            status_msg += f"\\n• {cap.replace('_', ' ').title()}: {status}"
        
        status_msg += f"\\n\\n**Personality:** {', '.join(personality['traits']['core_traits'])}"
        status_msg += f"\\n**Session ID:** {personality['session_id']}"
        
        return status_msg
    
    async def _handle_action_command(self, action: str) -> str:
        """Handle action execution command."""
        try:
            # Use The Emulator to process the action
            decision = self.emulator.get_decision(f"Execute this action: {action}")
            
            # For now, return the AI's decision about the action
            # In a full implementation, this would execute actual system commands
            return f"🎯 **Action Analysis:** {action}\\n\\n🧠 **AI Response:** {decision}\\n\\n⚠️ *Note: Actual system execution requires additional security implementation.*"
            
        except Exception as e:
            logger.error(f"Error handling action command: {e}")
            return f"❌ Error processing action: {action}"
    
    async def _keepalive_task(self):
        """Background keepalive task."""
        while True:
            try:
                await asyncio.sleep(self.keepalive_interval)
                
                # Simple sync to keep connection alive
                if self.client:
                    await self.client.sync(timeout=5000, full_state=False)
                    logger.debug("Keepalive sync completed")
                    
            except Exception as e:
                logger.debug(f"Keepalive error: {e}")
                await asyncio.sleep(10)
    
    def _display_startup_info(self, device_id: str):
        """Display startup information."""
        print("=" * 60)
        print("🤖 The Emulator Matrix Bot - ACTIVE!")
        print("=" * 60)
        print(f"✅ Identity: {self.username}")
        print(f"✅ Bot Name: {self.bot_name}")
        print(f"🔑 Device ID: {device_id}")
        print(f"🏠 Homeserver: {self.homeserver}")
        print(f"📍 Joined Rooms: {len(self.joined_rooms)}")
        print("✅ Auto-accepting room invites")
        print(f"📝 Triggers: '{self.bot_name}', 'emulator'")
        print("💬 Reply to my messages to continue conversations")
        print("🔄 Reset: '!reset' to clear context")
        print("📚 Help: ?help for all commands")
        print("")
        print("🔐 **Authorized Users:**")
        for user in self.authorized_users:
            print(f"   • {user}")
        print("")
        print("⚡ **Available Commands:**")
        print("   • ?help - Show help")
        print("   • ?sys - System status (authorized only)")
        print("   • ?status - Bot status (authorized only)")
        print("   • ?command <action> - Execute actions (authorized only)")
        print("")
        print("🧠 **AI Capabilities:**")
        capabilities = self.emulator.get_capabilities()
        for cap, enabled in capabilities.items():
            status = "✅" if enabled else "❌"
            print(f"   • {cap.replace('_', ' ').title()}: {status}")
        print("")
        personality = self.emulator.get_personality_info()
        print(f"🎭 **Personality:** {', '.join(personality['traits']['core_traits'])}")
        print("=" * 60)
        print("🚀 Ready for intelligent automation!")
        print("=" * 60)


# Main execution function
async def main():
    """Main function to run The Emulator Matrix Bot."""
    # Configuration from environment variables
    homeserver = os.getenv("MATRIX_HOMESERVER", "https://envs.net")
    username = os.getenv("MATRIX_USERNAME", "@ribit.2.0:envs.net")
    password = os.getenv("MATRIX_PASSWORD", "")
    
    if not password:
        print("❌ ERROR: MATRIX_PASSWORD environment variable not set!")
        print("Please set your Matrix password in the environment:")
        print("export MATRIX_PASSWORD='your_password_here'")
        return
    
    # Create and start the bot
    bot = EmulatorMatrixBot(homeserver, username, password)
    await bot.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\\n👋 The Emulator Matrix Bot shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
