#!/usr/bin/env python3
"""
The Emulator Matrix Bot Runner

Easy deployment script for running The Emulator as a Matrix chatbot
with the specified user handles and command system.

Usage:
    python run_matrix_bot.py

Environment Variables:
    MATRIX_HOMESERVER - Matrix homeserver URL (default: https://envs.net)
    MATRIX_USERNAME - Bot username (default: @ribit.2.0:envs.net)
    MATRIX_PASSWORD - Bot password (required)
"""

import asyncio
import os
import sys
import logging
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from emulator.matrix_bot import EmulatorMatrixBot
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you're running from the project root directory")
    print("and that all dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_environment():
    """Load environment variables from .env file if it exists."""
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        print(f"📄 Loading environment from {env_file}")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


def validate_configuration():
    """Validate Matrix configuration."""
    homeserver = os.getenv("MATRIX_HOMESERVER", "https://envs.net")
    username = os.getenv("MATRIX_USERNAME", "@ribit.2.0:envs.net")
    password = os.getenv("MATRIX_PASSWORD", "")
    
    print("🔧 Matrix Configuration:")
    print(f"   Homeserver: {homeserver}")
    print(f"   Username: {username}")
    print(f"   Password: {'✅ Set' if password else '❌ Not Set'}")
    
    if not password:
        print("\\n❌ ERROR: MATRIX_PASSWORD environment variable not set!")
        print("\\nPlease set your Matrix password:")
        print("\\n1. Create a .env file in the project root:")
        print("   MATRIX_HOMESERVER=https://envs.net")
        print("   MATRIX_USERNAME=@ribit.2.0:envs.net")
        print("   MATRIX_PASSWORD=your_password_here")
        print("\\n2. Or set environment variable:")
        print("   export MATRIX_PASSWORD='your_password_here'")
        return False
    
    return True


async def main():
    """Main function to run The Emulator Matrix Bot."""
    print("🤖 The Emulator Matrix Bot Runner")
    print("=" * 50)
    
    # Load environment
    load_environment()
    
    # Validate configuration
    if not validate_configuration():
        return
    
    # Get configuration
    homeserver = os.getenv("MATRIX_HOMESERVER", "https://envs.net")
    username = os.getenv("MATRIX_USERNAME", "@ribit.2.0:envs.net")
    password = os.getenv("MATRIX_PASSWORD")
    
    # Define authorized users
    authorized_users = {
        "@rabit233:matrix.anarchists.space",
        "@rabit232:envs.net"
    }
    
    print("\\n🔐 Authorized Command Users:")
    for user in authorized_users:
        print(f"   • {user}")
    
    print("\\n🚀 Starting The Emulator Matrix Bot...")
    
    try:
        # Create and start the bot
        bot = EmulatorMatrixBot(
            homeserver=homeserver,
            username=username,
            password=password,
            authorized_users=authorized_users
        )
        
        await bot.start()
        
    except KeyboardInterrupt:
        print("\\n👋 The Emulator Matrix Bot shutting down...")
    except Exception as e:
        logger.error(f"Bot error: {e}")
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    # Run the bot
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
