#!/usr/bin/env python3
"""
SafePal Wallet Balance Checker - Advanced Version
This version includes better error handling, logging, and Chrome profile support
"""

import time
import os
import sys
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Configuration
EXTENSION_ID = "lgmpcpglpngdoalbgeoldeajfclnhafa"
VALID_SEEDS_FILE = "valid.txt"
BALANCE_OUTPUT_FILE = "balance.txt"
LOG_FILE = "safepal_checker.log"
WAIT_TIMEOUT = 30
BALANCE_CHECK_WAIT = 10  # seconds to wait for balance to load

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class SafePalAdvancedAutomation:
    def __init__(self, chrome_profile_path=None):
        """Initialize the SafePal automation with Chrome WebDriver"""
        self.chrome_profile_path = chrome_profile_path
        self.driver = None
        self.wait = None
        self.processed_count = 0
        self.success_count = 0
        self.error_count = 0
        
    def setup_driver(self):
        """Set up Chrome WebDriver with SafePal extension"""
        chrome_options = Options()
        
        # Use existing Chrome profile if provided
        if self.chrome_profile_path and os.path.exists(self.chrome_profile_path):
            chrome_options.add_argument(f'--user-data-dir={self.chrome_profile_path}')
            logger.info(f"Using Chrome profile: {self.chrome_profile_path}")
        
        # Additional Chrome options for stability
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Disable images for faster loading (optional)
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, WAIT_TIMEOUT)
            logger.info("Chrome WebDriver initialized successfully")
            return True
        except WebDriverException as e:
            logger.error(f"Failed to initialize WebDriver: {str(e)}")
            return False
        
    def open_extension(self):
        """Navigate to SafePal extension popup"""
        try:
            extension_url = f"chrome-extension://{EXTENSION_ID}/index.html"
            self.driver.get(extension_url)
            logger.info(f"Navigating to extension: {extension_url}")
            time.sleep(3)
            return True
        except Exception as e:
            logger.error(f"Failed to open extension: {str(e)}")
            return False
    
    def wait_and_click(self, xpath, timeout=10, description="element"):
        """Wait for element and click it"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            logger.debug(f"Clicked {description}")
            return True
        except TimeoutException:
            logger.warning(f"Timeout waiting for {description}: {xpath}")
            return False
        except Exception as e:
            logger.error(f"Error clicking {description}: {str(e)}")
            return False
    
    def wait_and_input(self, xpath, text, timeout=10, description="input field"):
        """Wait for input element and enter text"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element.clear()
            element.send_keys(text)
            logger.debug(f"Entered text in {description}")
            return True
        except TimeoutException:
            logger.warning(f"Timeout waiting for {description}: {xpath}")
            return False
        except Exception as e:
            logger.error(f"Error entering text in {description}: {str(e)}")
            return False
    
    def take_screenshot(self, name="screenshot"):
        """Take a screenshot for debugging"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            self.driver.save_screenshot(filename)
            logger.info(f"Screenshot saved: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            return None
    
    def import_seed_phrase(self, seed_phrase):
        """Import a seed phrase into SafePal wallet"""
        try:
            logger.info(f"Importing seed phrase: {seed_phrase[:30]}...")
            
            # Navigate to extension
            if not self.open_extension():
                return False
            
            # Try multiple possible button texts and selectors
            add_wallet_selectors = [
                "//button[contains(text(), 'Add Wallet')]",
                "//div[contains(text(), 'Add Wallet')]",
                "//span[contains(text(), 'Add Wallet')]",
                "//*[contains(@class, 'add-wallet')]"
            ]
            
            clicked = False
            for selector in add_wallet_selectors:
                if self.wait_and_click(selector, timeout=5, description="Add Wallet button"):
                    clicked = True
                    break
            
            if not clicked:
                # Try "My Wallet" first
                my_wallet_selectors = [
                    "//button[contains(text(), 'My Wallet')]",
                    "//div[contains(text(), 'My Wallet')]",
                    "//span[contains(text(), 'My Wallet')]"
                ]
                
                for selector in my_wallet_selectors:
                    if self.wait_and_click(selector, timeout=5, description="My Wallet button"):
                        time.sleep(2)
                        # Then try Add Wallet again
                        for add_selector in add_wallet_selectors:
                            if self.wait_and_click(add_selector, timeout=5, description="Add Wallet button"):
                                clicked = True
                                break
                        break
            
            if not clicked:
                logger.error("Could not find Add Wallet button")
                self.take_screenshot("error_add_wallet")
                return False
            
            time.sleep(2)
            
            # Click "Import Wallet"
            import_selectors = [
                "//button[contains(text(), 'Import Wallet')]",
                "//div[contains(text(), 'Import Wallet')]",
                "//span[contains(text(), 'Import Wallet')]",
                "//button[contains(text(), 'Import')]",
                "//*[contains(@class, 'import-wallet')]"
            ]
            
            clicked = False
            for selector in import_selectors:
                if self.wait_and_click(selector, timeout=10, description="Import Wallet button"):
                    clicked = True
                    break
            
            if not clicked:
                logger.error("Could not find Import Wallet button")
                self.take_screenshot("error_import_wallet")
                return False
            
            time.sleep(2)
            
            # Click "Mnemonic phrase"
            mnemonic_selectors = [
                "//button[contains(text(), 'Mnemonic')]",
                "//div[contains(text(), 'Mnemonic')]",
                "//span[contains(text(), 'Mnemonic')]",
                "//button[contains(text(), 'Seed')]",
                "//*[contains(@class, 'mnemonic')]"
            ]
            
            clicked = False
            for selector in mnemonic_selectors:
                if self.wait_and_click(selector, timeout=10, description="Mnemonic button"):
                    clicked = True
                    break
            
            if not clicked:
                logger.error("Could not find Mnemonic button")
                self.take_screenshot("error_mnemonic")
                return False
            
            time.sleep(2)
            
            # Click "Next" if needed
            next_selectors = [
                "//button[contains(text(), 'Next')]",
                "//button[contains(text(), 'Continue')]"
            ]
            
            for selector in next_selectors:
                self.wait_and_click(selector, timeout=3, description="Next button")
            
            time.sleep(1)
            
            # Enter seed phrase
            input_selectors = [
                "//textarea",
                "//input[@type='text' and contains(@placeholder, 'mnemonic')]",
                "//input[@type='text' and contains(@placeholder, 'seed')]",
                "//input[@type='text']"
            ]
            
            entered = False
            for selector in input_selectors:
                if self.wait_and_input(selector, seed_phrase, timeout=10, description="Seed phrase input"):
                    entered = True
                    break
            
            if not entered:
                logger.error("Could not find seed phrase input field")
                self.take_screenshot("error_seed_input")
                return False
            
            time.sleep(1)
            
            # Click "Import" or "Next" button
            submit_selectors = [
                "//button[contains(text(), 'Import')]",
                "//button[contains(text(), 'Next')]",
                "//button[contains(text(), 'Continue')]",
                "//button[@type='submit']"
            ]
            
            clicked = False
            for selector in submit_selectors:
                if self.wait_and_click(selector, timeout=10, description="Import/Submit button"):
                    clicked = True
                    break
            
            if not clicked:
                logger.error("Could not find Import/Submit button")
                self.take_screenshot("error_submit")
                return False
            
            time.sleep(3)
            
            # Handle wallet name if prompted
            try:
                name_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Wallet name'] | //input[@type='text']")
                name_input.clear()
                name_input.send_keys(f"Wallet_{int(time.time())}")
                
                continue_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')] | //button[contains(text(), 'Confirm')]")
                continue_btn.click()
                time.sleep(2)
            except:
                pass
            
            logger.info("Seed phrase imported successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to import seed phrase: {str(e)}")
            self.take_screenshot("error_import")
            return False
    
    def check_balance(self):
        """Check wallet balance with improved detection"""
        try:
            logger.info("Checking wallet balance...")
            
            # Wait for wallet to load
            time.sleep(BALANCE_CHECK_WAIT)
            
            # Take screenshot for manual verification if needed
            self.take_screenshot("balance_check")
            
            # Multiple strategies to find balance
            balance_found = False
            balance_value = 0.0
            
            # Strategy 1: Look for USD/dollar amounts
            try:
                balance_elements = self.driver.find_elements(By.XPATH, 
                    "//*[contains(text(), '$')] | //*[contains(text(), 'USD')] | //*[contains(@class, 'balance')] | //*[contains(@class, 'total')]"
                )
                
                import re
                for element in balance_elements:
                    text = element.text.strip()
                    if text:
                        logger.debug(f"Found potential balance element: {text}")
                        
                        # Extract numeric value
                        numbers = re.findall(r'[\d,]+\.?\d*', text.replace(',', ''))
                        if numbers:
                            try:
                                value = float(numbers[0])
                                if value > 0:
                                    logger.info(f"Balance found: ${value}")
                                    balance_found = True
                                    balance_value = value
                                    break
                            except ValueError:
                                continue
            except Exception as e:
                logger.debug(f"Strategy 1 failed: {str(e)}")
            
            # Strategy 2: Look for crypto amounts (BTC, ETH, etc.)
            if not balance_found:
                try:
                    crypto_elements = self.driver.find_elements(By.XPATH,
                        "//*[contains(text(), 'BTC')] | //*[contains(text(), 'ETH')] | //*[contains(text(), 'BNB')]"
                    )
                    
                    for element in crypto_elements:
                        text = element.text.strip()
                        if text and any(char.isdigit() for char in text):
                            logger.info(f"Crypto balance found: {text}")
                            balance_found = True
                            balance_value = 1.0  # Mark as having balance
                            break
                except Exception as e:
                    logger.debug(f"Strategy 2 failed: {str(e)}")
            
            # Strategy 3: Check page source for balance indicators
            if not balance_found:
                try:
                    page_source = self.driver.page_source.lower()
                    if 'balance' in page_source and ('btc' in page_source or 'eth' in page_source):
                        logger.info("Balance indicators found in page source")
                        # This is a weak signal, but might indicate balance
                        # Manual verification recommended
                except Exception as e:
                    logger.debug(f"Strategy 3 failed: {str(e)}")
            
            if balance_found and balance_value > 0:
                logger.info(f"SUCCESS: Balance detected: {balance_value}")
                return True, balance_value
            else:
                logger.info("No balance found or balance is 0")
                return False, 0
            
        except Exception as e:
            logger.error(f"Failed to check balance: {str(e)}")
            return False, 0
    
    def process_seed_phrases(self, seed_file, output_file):
        """Process all seed phrases from file"""
        # Read seed phrases
        if not os.path.exists(seed_file):
            logger.error(f"Seed file not found: {seed_file}")
            return
        
        with open(seed_file, 'r') as f:
            seed_phrases = [line.strip() for line in f if line.strip()]
        
        logger.info(f"Found {len(seed_phrases)} seed phrases to process")
        
        # Clear output file
        with open(output_file, 'w') as f:
            f.write("")
        
        # Process each seed phrase
        for idx, seed_phrase in enumerate(seed_phrases, 1):
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing seed {idx}/{len(seed_phrases)}")
            logger.info(f"{'='*60}")
            
            self.processed_count += 1
            
            # Import seed phrase
            if self.import_seed_phrase(seed_phrase):
                # Check balance
                has_balance, balance_value = self.check_balance()
                
                if has_balance:
                    logger.info(f"✓ Seed has balance: {balance_value}")
                    self.success_count += 1
                    
                    # Save to output file
                    with open(output_file, 'a') as f:
                        f.write(f"{seed_phrase}\n")
                else:
                    logger.info("✗ Seed has no balance")
            else:
                logger.error("✗ Failed to import seed phrase")
                self.error_count += 1
            
            # Pause between iterations
            if idx < len(seed_phrases):
                logger.info("Waiting before next seed...")
                time.sleep(3)
        
        # Final summary
        logger.info(f"\n{'='*60}")
        logger.info("PROCESSING COMPLETE")
        logger.info(f"{'='*60}")
        logger.info(f"Total processed: {self.processed_count}")
        logger.info(f"Seeds with balance: {self.success_count}")
        logger.info(f"Errors: {self.error_count}")
        logger.info(f"Results saved to: {output_file}")
        logger.info(f"Log saved to: {LOG_FILE}")
    
    def cleanup(self):
        """Close browser and cleanup"""
        if self.driver:
            logger.info("Closing browser...")
            try:
                self.driver.quit()
            except:
                pass


def main():
    """Main execution function"""
    print("=" * 60)
    print("SafePal Wallet Balance Checker - Advanced Version")
    print("=" * 60)
    
    # Initialize automation
    automation = SafePalAdvancedAutomation()
    
    try:
        # Setup WebDriver
        if not automation.setup_driver():
            logger.error("Failed to setup WebDriver. Exiting...")
            return
        
        logger.info("\n" + "="*60)
        logger.info("IMPORTANT: Manual Setup Required")
        logger.info("="*60)
        logger.info("1. Install SafePal Extension from Chrome Web Store")
        logger.info("2. Complete initial setup if needed")
        logger.info("3. Make sure valid.txt contains your seed phrases")
        logger.info("4. Press Enter to start processing...")
        logger.info("="*60)
        input()
        
        # Process seed phrases
        automation.process_seed_phrases(VALID_SEEDS_FILE, BALANCE_OUTPUT_FILE)
        
    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user")
    except Exception as e:
        logger.error(f"\nUnexpected error: {str(e)}", exc_info=True)
    finally:
        # Cleanup
        automation.cleanup()


if __name__ == "__main__":
    main()
