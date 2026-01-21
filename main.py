"""
Main entry point for HR Management System.
Initializes all components and starts the Telegram bot.
"""

import logging
import sys
from config import config
from database import db_handler
from bot import main as start_bot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hr_system.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def validate_environment() -> bool:
    """Validate that all required environment variables and connections are working."""
    try:
        logger.info("Validating environment configuration...")
        
        # Validate config
        config.validate()
        logger.info("✓ Configuration validated")
        
        # Test database connection
        if db_handler.client:
            logger.info("✓ Database connection successful")
        else:
            logger.error("✗ Database connection failed")
            return False
        
        logger.info("✓ Environment validation successful")
        return True
    
    except Exception as e:
        logger.error(f"✗ Environment validation failed: {e}")
        return False


def main():
    """Main application entry point."""
    try:
        logger.info("=" * 60)
        logger.info("HR Management System Starting...")
        logger.info("=" * 60)
        
        # Validate environment
        if not validate_environment():
            logger.error("Environment validation failed. Please check your configuration.")
            sys.exit(1)
        
        logger.info("All systems operational. Starting Telegram bot...")
        
        # Start the Telegram bot
        start_bot()
    
    except KeyboardInterrupt:
        logger.info("\nShutting down gracefully...")
        db_handler.close()
        logger.info("HR Management System stopped")
        sys.exit(0)
    
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        db_handler.close()
        sys.exit(1)


if __name__ == "__main__":
    main()