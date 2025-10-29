#!/usr/bin/env python3
"""
SafePal Wallet Balance Checker - Final Production Version
Optimized for chrome-extension://lgmpcpglpngdoalbgeoldeajfclnhafa/index.html#/import/mnemonics
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
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configuration
EXTENSION_ID = "lgmpcpglpngdoalbgeoldeajfclnhafa"
IMPORT_URL = f"chrome-extension://{EXTENSION_ID}/index.html#/import/mnemonics"
MAIN_URL = f"chrome-extension://{EXTENSION_ID}/index.html"
VALID_SEEDS_FILE = "valid.txt"
BALANCE_OUTPUT_FILE = "balance.txt"
LOG_FILE = "safepal_final.log"
WAIT_TIMEOUT = 20
BALANCE_WAIT = 10

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


class SafePalFinalAutomation:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.processed = 0
        self.with_balance = 0
        
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--start-maximized')
        # Remove headless for visible operation
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, WAIT_TIMEOUT)
            logger.info("✓ Chrome WebDriver initialized")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to initialize Chrome: {e}")
            return False
    
    def screenshot(self, name):
        """Take screenshot"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            self.driver.save_screenshot(filename)
            logger.info(f"  📸 Screenshot: {filename}")
            return filename
        except:
            return None
    
    def navigate_to_import(self):
        """Navigate directly to import mnemonics page"""
        try:
            logger.info(f"Navigating to: {IMPORT_URL}")
            self.driver.get(IMPORT_URL)
            time.sleep(3)
            
            # Check if extension is accessible
            if "chrome-extension" not in self.driver.current_url:
                logger.error("✗ SafePal extension not accessible!")
                logger.error("  Please install SafePal extension first")
                return False
            
            logger.info("✓ SafePal extension accessible")
            return True
        except Exception as e:
            logger.error(f"✗ Navigation failed: {e}")
            return False
    
    def import_seed_phrase(self, seed_phrase):
        """Import seed phrase using SafePal's import page"""
        try:
            logger.info(f"Importing: {seed_phrase[:30]}...")
            
            # Navigate to import page
            if not self.navigate_to_import():
                return False
            
            time.sleep(2)
            self.screenshot("01_import_page")
            
            # Split seed into words
            words = seed_phrase.split()
            logger.info(f"  Words: {len(words)}")
            
            # Find all input fields
            inputs = self.driver.find_elements(By.XPATH, "//input[@type='text']")
            textareas = self.driver.find_elements(By.XPATH, "//textarea")
            
            logger.info(f"  Found {len(inputs)} inputs, {len(textareas)} textareas")
            
            success = False
            
            # Method 1: Individual input boxes (SafePal typically uses this)
            if len(inputs) >= len(words):
                logger.info(f"  Method: Individual inputs")
                for idx, word in enumerate(words):
                    try:
                        # Clear and enter word
                        inputs[idx].clear()
                        inputs[idx].send_keys(word)
                        time.sleep(0.2)
                    except Exception as e:
                        logger.warning(f"  Word {idx+1} error: {e}")
                success = True
                logger.info(f"  ✓ Entered {len(words)} words")
            
            # Method 2: Single textarea
            elif textareas:
                logger.info(f"  Method: Single textarea")
                textareas[0].clear()
                textareas[0].send_keys(seed_phrase)
                success = True
                logger.info(f"  ✓ Entered full phrase")
            
            # Method 3: Try any visible input
            else:
                all_inputs = self.driver.find_elements(By.TAG_NAME, "input")
                if all_inputs:
                    logger.info(f"  Method: First available input")
                    all_inputs[0].send_keys(seed_phrase)
                    success = True
                    logger.info(f"  ✓ Entered phrase")
            
            if not success:
                logger.error("  ✗ No suitable input found")
                self.screenshot("error_no_input")
                return False
            
            time.sleep(1)
            self.screenshot("02_phrase_entered")
            
            # Click submit button
            logger.info("  Looking for submit button...")
            button_found = False
            
            # Try different button texts
            for btn_text in ['Import', 'Next', 'Continue', 'Confirm', 'import', 'next']:
                try:
                    button = self.wait.until(EC.element_to_be_clickable((
                        By.XPATH, 
                        f"//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{btn_text.lower()}')]"
                    )))
                    logger.info(f"  Found button: '{button.text}'")
                    button.click()
                    logger.info(f"  ✓ Clicked button")
                    button_found = True
                    break
                except:
                    continue
            
            if not button_found:
                # Try any button
                try:
                    buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    for btn in buttons:
                        if btn.text and btn.is_displayed():
                            logger.info(f"  Trying button: '{btn.text}'")
                            btn.click()
                            button_found = True
                            break
                except:
                    pass
            
            if not button_found:
                logger.warning("  ⚠ No button clicked - may need manual intervention")
            
            time.sleep(4)
            self.screenshot("03_after_submit")
            
            # Handle wallet name if prompted
            try:
                name_inputs = self.driver.find_elements(By.XPATH, "//input[@type='text']")
                if name_inputs:
                    name_inputs[0].clear()
                    name_inputs[0].send_keys(f"Wallet_{int(time.time())}")
                    
                    # Click continue/confirm
                    for btn_text in ['Continue', 'Confirm', 'OK']:
                        try:
                            btn = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{btn_text}')]")
                            btn.click()
                            break
                        except:
                            continue
            except:
                pass
            
            logger.info("✓ Import completed")
            return True
            
        except Exception as e:
            logger.error(f"✗ Import failed: {e}")
            self.screenshot("error_import")
            return False
    
    def check_balance(self):
        """Check wallet balance"""
        try:
            logger.info("Checking balance...")
            
            # Wait for wallet to load
            time.sleep(BALANCE_WAIT)
            
            self.screenshot("04_balance_check")
            
            # Navigate to main wallet page
            try:
                self.driver.get(MAIN_URL)
                time.sleep(3)
            except:
                pass
            
            # Multiple detection strategies
            has_balance = False
            balance_value = 0.0
            
            # Strategy 1: Look for dollar amounts
            try:
                elements = self.driver.find_elements(By.XPATH, 
                    "//*[contains(text(), '$')] | "
                    "//*[contains(text(), 'USD')] | "
                    "//*[contains(@class, 'balance')] | "
                    "//*[contains(@class, 'amount')]"
                )
                
                import re
                for elem in elements:
                    text = elem.text.strip()
                    if text:
                        logger.debug(f"  Found: {text}")
                        numbers = re.findall(r'[\d,]+\.?\d*', text.replace(',', ''))
                        if numbers:
                            try:
                                val = float(numbers[0])
                                if val > 0:
                                    logger.info(f"  💰 Balance: ${val}")
                                    has_balance = True
                                    balance_value = val
                                    break
                            except:
                                continue
            except Exception as e:
                logger.debug(f"  Strategy 1 failed: {e}")
            
            # Strategy 2: Look for crypto amounts
            if not has_balance:
                try:
                    crypto_elements = self.driver.find_elements(By.XPATH,
                        "//*[contains(text(), 'BTC')] | "
                        "//*[contains(text(), 'ETH')] | "
                        "//*[contains(text(), 'BNB')] | "
                        "//*[contains(text(), 'USDT')]"
                    )
                    
                    for elem in crypto_elements:
                        text = elem.text.strip()
                        if text and any(c.isdigit() for c in text):
                            # Check if there's a non-zero number
                            import re
                            numbers = re.findall(r'[\d.]+', text)
                            if numbers:
                                try:
                                    val = float(numbers[0])
                                    if val > 0:
                                        logger.info(f"  💰 Crypto balance found: {text}")
                                        has_balance = True
                                        balance_value = val
                                        break
                                except:
                                    continue
                except Exception as e:
                    logger.debug(f"  Strategy 2 failed: {e}")
            
            # Strategy 3: Check page source
            if not has_balance:
                try:
                    page_source = self.driver.page_source.lower()
                    # Look for balance indicators
                    if 'balance' in page_source:
                        # Check if there are numbers near "balance"
                        import re
                        balance_pattern = re.findall(r'balance["\s:>]+(\d+\.?\d*)', page_source)
                        if balance_pattern:
                            logger.info(f"  Found balance pattern in source")
                except Exception as e:
                    logger.debug(f"  Strategy 3 failed: {e}")
            
            self.screenshot("05_final_balance")
            
            if has_balance:
                logger.info(f"✓ BALANCE DETECTED: {balance_value}")
                return True, balance_value
            else:
                logger.info("✗ No balance detected")
                return False, 0
                
        except Exception as e:
            logger.error(f"✗ Balance check failed: {e}")
            return False, 0
    
    def process_seeds(self, input_file, output_file):
        """Process all seed phrases"""
        # Read seeds
        if not os.path.exists(input_file):
            logger.error(f"Input file not found: {input_file}")
            return
        
        with open(input_file, 'r') as f:
            seeds = [line.strip() for line in f if line.strip()]
        
        logger.info(f"Found {len(seeds)} seed phrases to process")
        
        # Clear output
        with open(output_file, 'w') as f:
            f.write("")
        
        # Process each seed
        for idx, seed in enumerate(seeds, 1):
            logger.info(f"\n{'='*70}")
            logger.info(f"SEED {idx}/{len(seeds)}")
            logger.info(f"{'='*70}")
            
            self.processed += 1
            
            if self.import_seed_phrase(seed):
                has_bal, val = self.check_balance()
                
                if has_bal:
                    logger.info(f"✓✓✓ SEED HAS BALANCE: {val}")
                    self.with_balance += 1
                    
                    # Save to output
                    with open(output_file, 'a') as f:
                        f.write(f"{seed}\n")
                else:
                    logger.info("--- Seed has no balance")
            else:
                logger.error("✗✗✗ Import failed")
            
            # Wait between seeds
            if idx < len(seeds):
                logger.info("Waiting 3 seconds...")
                time.sleep(3)
        
        # Summary
        logger.info(f"\n{'='*70}")
        logger.info("PROCESSING COMPLETE")
        logger.info(f"{'='*70}")
        logger.info(f"Total processed: {self.processed}")
        logger.info(f"With balance: {self.with_balance}")
        logger.info(f"Results saved to: {output_file}")
    
    def cleanup(self):
        """Close browser"""
        if self.driver:
            logger.info("Closing browser...")
            try:
                self.driver.quit()
            except:
                pass


def main():
    """Main function"""
    print("=" * 70)
    print("SafePal Wallet Balance Checker - FINAL VERSION")
    print("=" * 70)
    print("\nOptimized for: chrome-extension://lgmpcpglpngdoalbgeoldeajfclnhafa")
    print()
    
    automation = SafePalAdvancedAutomation()
    
    try:
        # Setup
        if not automation.setup_driver():
            logger.error("Failed to setup WebDriver")
            return
        
        logger.info("\n" + "="*70)
        logger.info("IMPORTANT: Prerequisites")
        logger.info("="*70)
        logger.info("1. SafePal Extension must be installed in Chrome")
        logger.info("2. valid.txt must contain your seed phrases")
        logger.info("3. Chrome will open in VISIBLE mode")
        logger.info("="*70)
        logger.info("\nPress Enter to start...")
        input()
        
        # Process
        automation.process_seeds(VALID_SEEDS_FILE, BALANCE_OUTPUT_FILE)
        
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
    except Exception as e:
        logger.error(f"\nError: {e}", exc_info=True)
    finally:
        automation.cleanup()


if __name__ == "__main__":
    main()
