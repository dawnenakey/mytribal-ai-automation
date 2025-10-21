#!/usr/bin/env python3
"""
Daily Automation for mytribal.ai
Combines content generation and publishing in one script
"""

import subprocess
import sys
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('daily_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_content_generation():
    """Run the daily AI content generator"""
    try:
        logger.info("🚀 Starting content generation...")
        result = subprocess.run(
            [sys.executable, 'daily_ai_content_generator.py'],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        
        if result.returncode == 0:
            logger.info("✅ Content generation completed successfully")
            return True
        else:
            logger.error(f"❌ Content generation failed: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error in content generation: {e}")
        return False

def run_publishing():
    """Run the WordPress REST publisher"""
    try:
        logger.info("📤 Starting content publishing...")
        result = subprocess.run(
            [sys.executable, 'wordpress_rest_publisher.py'],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        
        if result.returncode == 0:
            logger.info("✅ Publishing completed successfully")
            return True
        else:
            logger.error(f"❌ Publishing failed: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error in publishing: {e}")
        return False

def main():
    """Main automation workflow"""
    logger.info("🎯 Starting Daily Automation for mytribal.ai")
    logger.info(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Generate content
    if not run_content_generation():
        logger.error("❌ Content generation failed. Stopping automation.")
        return False
    
    # Step 2: Publish content
    if not run_publishing():
        logger.error("❌ Publishing failed. Content generated but not published.")
        return False
    
    logger.info("🎉 Daily automation completed successfully!")
    logger.info(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
