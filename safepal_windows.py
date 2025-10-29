#!/usr/bin/env python3
"""
SafePal Wallet Balance Checker - Windows Compatible Version
No Unicode emojis - works on Windows console
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
PASSWORD_SETUP_URL = f"chrome-extension://{EXTENSION_ID}/index.html#/password?redirect=/import-wallet"
IMPORT_URL = f"chrome-extension://{EXTENSION_ID}/index.html#/import/mnemonics"
MAIN_URL = f"chrome-extension://{EXTENSION_ID}/index.html"
VALID_SEEDS_FILE = "valid.txt"
BALANCE_OUTPUT_FILE = "balance.txt"
LOG_FILE = "safepal_windows.log"
WAIT_TIMEOUT = 20
BALANCE_WAIT = 10

# SafePal wallet password (for encryption)
WALLET_PASSWORD = "Apple2020"

# Setup logging with UTF-8 encoding for Windows
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class SafePalWindowsAutomation:
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
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, WAIT_TIMEOUT)
            logger.info("[OK] Chrome WebDriver initialized")
            return True
        except Exception as e:
            logger.error(f"[ERROR] Failed to initialize Chrome: {e}")
            return False
    
    def setup_password_first_time(self):
        """Setup SafePal password on first run"""
        try:
            logger.info("Setting up SafePal password...")
            logger.info(f"Navigating to: {PASSWORD_SETUP_URL}")
            self.driver.get(PASSWORD_SETUP_URL)
            time.sleep(3)
            
            self.screenshot("00_password_setup")
            
            # Look for password input fields
            password_fields = self.driver.find_elements(By.XPATH, "//input[@type='password']")
            
            if len(password_fields) >= 2:
                logger.info(f"  Found {len(password_fields)} password fields")
                
                # Enter password (usually 2 fields: password + confirm)
                for idx, field in enumerate(password_fields[:2]):
                    field.click()
                    time.sleep(0.1)
                    field.clear()
                    time.sleep(0.1)
                    field.send_keys(WALLET_PASSWORD)
                    logger.info(f"  [OK] Entered password in field {idx+1}")
                    time.sleep(0.2)
                
                self.screenshot("00_password_entered")
                
                # Click confirm/continue button
                for btn_text in ['Confirm', 'Continue', 'Next', 'Create', 'Submit']:
                    try:
                        button = self.driver.find_element(By.XPATH, 
                            f"//button[contains(text(), '{btn_text}')]")
                        button.click()
                        logger.info(f"  [OK] Clicked '{btn_text}' button")
                        time.sleep(3)
                        return True
                    except:
                        continue
                
                logger.info("  [OK] Password setup completed")
                return True
            else:
                logger.info("  No password setup needed (already configured)")
                return True
                
        except Exception as e:
            logger.warning(f"  Password setup error: {e}")
            return True  # Continue anyway
    
    def screenshot(self, name):
        """Take screenshot"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            self.driver.save_screenshot(filename)
            logger.info(f"  [SCREENSHOT] {filename}")
            return filename
        except:
            return None
    
    def enter_password(self, password):
        """Enter password if prompted by SafePal"""
        try:
            logger.info("Checking for password prompt...")
            time.sleep(2)
            
            # Look for password input fields
            password_fields = self.driver.find_elements(By.XPATH, "//input[@type='password']")
            
            if password_fields:
                logger.info(f"  Found {len(password_fields)} password fields")
                
                # Enter password in all password fields (usually 2: password + confirm)
                for idx, field in enumerate(password_fields[:2]):
                    field.click()
                    time.sleep(0.1)
                    field.clear()
                    time.sleep(0.1)
                    field.send_keys(password)
                    logger.info(f"  [OK] Entered password in field {idx+1}")
                    time.sleep(0.2)
                
                self.screenshot("password_entered")
                
                # Look for submit/confirm button
                for btn_text in ['Confirm', 'Continue', 'Next', 'Submit', 'OK']:
                    try:
                        button = self.driver.find_element(By.XPATH, 
                            f"//button[contains(text(), '{btn_text}')]")
                        button.click()
                        logger.info(f"  [OK] Clicked '{btn_text}' button")
                        time.sleep(2)
                        return True
                    except:
                        continue
                
                logger.warning("  [WARNING] No submit button found after password")
                return True
            else:
                logger.info("  No password prompt found")
                return True
                
        except Exception as e:
            logger.warning(f"  Password entry error: {e}")
            return True  # Continue anyway
    
    def navigate_to_import(self):
        """Navigate directly to import mnemonics page"""
        try:
            logger.info(f"Navigating to: {IMPORT_URL}")
            self.driver.get(IMPORT_URL)
            time.sleep(3)
            
            if "chrome-extension" not in self.driver.current_url:
                logger.error("[ERROR] SafePal extension not accessible!")
                logger.error("  Please install SafePal extension first")
                return False
            
            logger.info("[OK] SafePal extension accessible")
            return True
        except Exception as e:
            logger.error(f"[ERROR] Navigation failed: {e}")
            return False
    
    def import_seed_phrase(self, seed_phrase):
        """Import seed phrase using SafePal's import page"""
        try:
            logger.info(f"Importing: {seed_phrase[:30]}...")
            
            if not self.navigate_to_import():
                return False
            
            time.sleep(2)
            self.screenshot("01_import_page")
            
            words = seed_phrase.split()
            logger.info(f"  Words: {len(words)}")
            
            # Find all input fields - SafePal uses password-type inputs!
            text_inputs = self.driver.find_elements(By.XPATH, "//input[@type='text']")
            password_inputs = self.driver.find_elements(By.XPATH, "//input[@type='password']")
            textareas = self.driver.find_elements(By.XPATH, "//textarea")
            
            # Combine all inputs
            inputs = text_inputs + password_inputs
            
            logger.info(f"  Found {len(text_inputs)} text inputs, {len(password_inputs)} password inputs, {len(textareas)} textareas")
            
            success = False
            
            # Method 1: Individual input boxes
            if len(inputs) >= len(words):
                logger.info(f"  Method: Individual inputs")
                for idx, word in enumerate(words):
                    try:
                        # Click to focus
                        inputs[idx].click()
                        time.sleep(0.15)
                        
                        # Clear the field
                        inputs[idx].clear()
                        time.sleep(0.15)
                        
                        # Type the ENTIRE word at once (not character by character)
                        inputs[idx].send_keys(word)
                        time.sleep(0.3)
                        
                        # Press Tab to move to next field and trigger validation
                        from selenium.webdriver.common.keys import Keys
                        inputs[idx].send_keys(Keys.TAB)
                        time.sleep(0.2)
                        
                        logger.debug(f"    Word {idx+1}: {word}")
                    except Exception as e:
                        logger.warning(f"  Word {idx+1} error: {e}")
                success = True
                logger.info(f"  [OK] Entered {len(words)} words")
            
            # Method 2: Single textarea
            elif textareas:
                logger.info(f"  Method: Single textarea")
                textareas[0].clear()
                textareas[0].send_keys(seed_phrase)
                success = True
                logger.info(f"  [OK] Entered full phrase")
            
            # Method 3: Try finding any input (last resort)
            else:
                all_inputs = self.driver.find_elements(By.TAG_NAME, "input")
                if all_inputs:
                    logger.warning(f"  Method: Fallback - found {len(all_inputs)} total inputs")
                    logger.warning(f"  This may not work correctly!")
                    all_inputs[0].send_keys(seed_phrase)
                    success = True
                    logger.info(f"  [OK] Entered phrase in first input")
            
            if not success:
                logger.error("  [ERROR] No suitable input found")
                self.screenshot("error_no_input")
                return False
            
            time.sleep(1)
            self.screenshot("02_phrase_entered")
            
            # Click submit button
            logger.info("  Looking for submit button...")
            button_found = False
            
            for btn_text in ['Import', 'Next', 'Continue', 'Confirm', 'import', 'next']:
                try:
                    button = self.wait.until(EC.element_to_be_clickable((
                        By.XPATH, 
                        f"//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{btn_text.lower()}')]"
                    )))
                    logger.info(f"  Found button: '{button.text}'")
                    button.click()
                    logger.info(f"  [OK] Clicked button")
                    button_found = True
                    break
                except:
                    continue
            
            if not button_found:
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
                logger.warning("  [WARNING] No button clicked - may need manual intervention")
            
            time.sleep(4)
            self.screenshot("03_after_submit")
            
            # Handle wallet name if prompted
            try:
                name_inputs = self.driver.find_elements(By.XPATH, "//input[@type='text']")
                if name_inputs:
                    name_inputs[0].clear()
                    name_inputs[0].send_keys(f"Wallet_{int(time.time())}")
                    
                    for btn_text in ['Continue', 'Confirm', 'OK']:
                        try:
                            btn = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{btn_text}')]")
                            btn.click()
                            break
                        except:
                            continue
            except:
                pass
            
            logger.info("[OK] Import completed")
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] Import failed: {e}")
            self.screenshot("error_import")
            return False
    
    def check_balance(self):
        """Check wallet balance"""
        try:
            logger.info("Checking balance...")
            
            time.sleep(BALANCE_WAIT)
            self.screenshot("04_balance_check")
            
            try:
                self.driver.get(MAIN_URL)
                time.sleep(3)
            except:
                pass
            
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
                                    logger.info(f"  [BALANCE] ${val}")
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
                            import re
                            numbers = re.findall(r'[\d.]+', text)
                            if numbers:
                                try:
                                    val = float(numbers[0])
                                    if val > 0:
                                        logger.info(f"  [BALANCE] Crypto: {text}")
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
                    if 'balance' in page_source:
                        import re
                        balance_pattern = re.findall(r'balance["\s:>]+(\d+\.?\d*)', page_source)
                        if balance_pattern:
                            logger.info(f"  Found balance pattern in source")
                except Exception as e:
                    logger.debug(f"  Strategy 3 failed: {e}")
            
            self.screenshot("05_final_balance")
            
            if has_balance:
                logger.info(f"[SUCCESS] BALANCE DETECTED: {balance_value}")
                return True, balance_value
            else:
                logger.info("[INFO] No balance detected")
                return False, 0
                
        except Exception as e:
            logger.error(f"[ERROR] Balance check failed: {e}")
            return False, 0
    
    def process_seeds(self, input_file, output_file):
        """Process all seed phrases"""
        if not os.path.exists(input_file):
            logger.error(f"Input file not found: {input_file}")
            return
        
        with open(input_file, 'r', encoding='utf-8') as f:
            seeds = [line.strip() for line in f if line.strip()]
        
        logger.info(f"Found {len(seeds)} seed phrases to process")
        
        # Setup password FIRST (only needed once)
        logger.info("\n" + "="*70)
        logger.info("STEP 1: Setting up SafePal password")
        logger.info("="*70)
        self.setup_password_first_time()
        time.sleep(2)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("")
        
        logger.info("\n" + "="*70)
        logger.info("STEP 2: Processing seeds")
        logger.info("="*70)
        
        for idx, seed in enumerate(seeds, 1):
            logger.info(f"\n{'='*70}")
            logger.info(f"SEED {idx}/{len(seeds)}")
            logger.info(f"{'='*70}")
            
            self.processed += 1
            
            if self.import_seed_phrase(seed):
                has_bal, val = self.check_balance()
                
                if has_bal:
                    logger.info(f"[SUCCESS] SEED HAS BALANCE: {val}")
                    self.with_balance += 1
                    
                    with open(output_file, 'a', encoding='utf-8') as f:
                        f.write(f"{seed}\n")
                else:
                    logger.info("[INFO] Seed has no balance")
            else:
                logger.error("[ERROR] Import failed")
            
            if idx < len(seeds):
                logger.info("Waiting 3 seconds...")
                time.sleep(3)
        
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
    print("SafePal Wallet Balance Checker - Windows Version")
    print("=" * 70)
    print("\nOptimized for: chrome-extension://lgmpcpglpngdoalbgeoldeajfclnhafa")
    print()
    
    automation = SafePalWindowsAutomation()
    
    try:
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
        
        automation.process_seeds(VALID_SEEDS_FILE, BALANCE_OUTPUT_FILE)
        
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
    except Exception as e:
        logger.error(f"\nError: {e}", exc_info=True)
    finally:
        automation.cleanup()


if __name__ == "__main__":
    main()
