#!/usr/bin/env python3
"""
SafePal Wallet Balance Checker
This script automates the process of importing seed phrases into SafePal wallet
and checking their balances using Selenium WebDriver.
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configuration
EXTENSION_ID = "lgmpcpglpngdoalbgeoldeajfclnhafa"
VALID_SEEDS_FILE = "valid.txt"
BALANCE_OUTPUT_FILE = "balance.txt"
WALLET_PASSWORD = "TestPassword123!"  # Default password for wallet
WAIT_TIMEOUT = 30  # seconds


class SafePalAutomation:
    def __init__(self, extension_path=None):
        """Initialize the SafePal automation with Chrome WebDriver"""
        self.extension_path = extension_path
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Set up Chrome WebDriver with SafePal extension"""
        chrome_options = Options()
        
        # Add extension if path provided
        if self.extension_path and os.path.exists(self.extension_path):
            chrome_options.add_argument(f'--load-extension={self.extension_path}')
            print(f"[INFO] Loading extension from: {self.extension_path}")
        else:
            print("[WARNING] Extension path not provided or doesn't exist.")
            print("[INFO] Please install SafePal extension manually in Chrome")
            print("[INFO] Extension ID: lgmpcpglpngdoalbgeoldeajfclnhafa")
        
        # Additional Chrome options
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize driver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, WAIT_TIMEOUT)
        print("[INFO] Chrome WebDriver initialized successfully")
        
    def open_extension(self):
        """Navigate to SafePal extension popup"""
        extension_url = f"chrome-extension://{EXTENSION_ID}/index.html"
        self.driver.get(extension_url)
        print(f"[INFO] Navigating to extension: {extension_url}")
        time.sleep(3)
        
    def import_seed_phrase(self, seed_phrase):
        """Import a seed phrase into SafePal wallet"""
        try:
            print(f"[INFO] Importing seed phrase: {seed_phrase[:20]}...")
            
            # Navigate to extension
            self.open_extension()
            
            # Click "My Wallet" or "Add Wallet" button
            # Note: These selectors may need to be updated based on actual extension UI
            try:
                # Try to find "Add Wallet" button
                add_wallet_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Wallet')] | //div[contains(text(), 'Add Wallet')]"))
                )
                add_wallet_btn.click()
                time.sleep(2)
            except TimeoutException:
                # If first time, might need to click "My Wallet" first
                try:
                    my_wallet_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'My Wallet')] | //div[contains(text(), 'My Wallet')]"))
                    )
                    my_wallet_btn.click()
                    time.sleep(2)
                    
                    add_wallet_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Wallet')] | //div[contains(text(), 'Add Wallet')]"))
                    )
                    add_wallet_btn.click()
                    time.sleep(2)
                except:
                    pass
            
            # Click "Import Wallet"
            import_wallet_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Import Wallet')] | //div[contains(text(), 'Import Wallet')]"))
            )
            import_wallet_btn.click()
            time.sleep(2)
            
            # Click "Mnemonic phrase"
            mnemonic_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Mnemonic')] | //div[contains(text(), 'Mnemonic')]"))
            )
            mnemonic_btn.click()
            time.sleep(2)
            
            # Enter seed phrase
            seed_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//textarea | //input[@type='text']"))
            )
            seed_input.clear()
            seed_input.send_keys(seed_phrase)
            time.sleep(1)
            
            # Click "Import" or "Next" button
            import_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Import')] | //button[contains(text(), 'Next')]"))
            )
            import_btn.click()
            time.sleep(3)
            
            # Set wallet name (optional)
            try:
                name_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Wallet name'] | //input[@type='text']")
                name_input.clear()
                name_input.send_keys("Imported Wallet")
                
                continue_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
                continue_btn.click()
                time.sleep(2)
            except:
                pass
            
            print("[INFO] Seed phrase imported successfully")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to import seed phrase: {str(e)}")
            return False
    
    def check_balance(self):
        """Check wallet balance"""
        try:
            print("[INFO] Checking wallet balance...")
            
            # Wait for wallet to load
            time.sleep(5)
            
            # Look for balance display elements
            # Note: These selectors need to be updated based on actual SafePal UI
            balance_elements = self.driver.find_elements(By.XPATH, 
                "//*[contains(text(), '$')] | //*[contains(text(), 'USD')] | //*[contains(@class, 'balance')]"
            )
            
            # Try to extract balance value
            for element in balance_elements:
                text = element.text.strip()
                if text and ('$' in text or 'USD' in text or any(char.isdigit() for char in text)):
                    print(f"[INFO] Found balance element: {text}")
                    
                    # Check if balance is greater than 0
                    # Extract numeric value
                    import re
                    numbers = re.findall(r'[\d.]+', text)
                    if numbers:
                        balance_value = float(numbers[0])
                        if balance_value > 0:
                            print(f"[SUCCESS] Balance found: {balance_value}")
                            return True, balance_value
            
            print("[INFO] No balance found or balance is 0")
            return False, 0
            
        except Exception as e:
            print(f"[ERROR] Failed to check balance: {str(e)}")
            return False, 0
    
    def remove_wallet(self):
        """Remove current wallet to prepare for next import"""
        try:
            print("[INFO] Removing wallet...")
            
            # Navigate to settings or wallet management
            # This is a placeholder - actual implementation depends on SafePal UI
            # You may need to manually remove wallets between imports
            
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to remove wallet: {str(e)}")
            return False
    
    def process_seed_phrases(self, seed_file, output_file):
        """Process all seed phrases from file"""
        # Read seed phrases
        if not os.path.exists(seed_file):
            print(f"[ERROR] Seed file not found: {seed_file}")
            return
        
        with open(seed_file, 'r') as f:
            seed_phrases = [line.strip() for line in f if line.strip()]
        
        print(f"[INFO] Found {len(seed_phrases)} seed phrases to process")
        
        # Clear output file
        with open(output_file, 'w') as f:
            f.write("")
        
        # Process each seed phrase
        successful_seeds = []
        
        for idx, seed_phrase in enumerate(seed_phrases, 1):
            print(f"\n[INFO] Processing seed {idx}/{len(seed_phrases)}")
            
            # Import seed phrase
            if self.import_seed_phrase(seed_phrase):
                # Check balance
                has_balance, balance_value = self.check_balance()
                
                if has_balance:
                    print(f"[SUCCESS] Seed has balance: {balance_value}")
                    successful_seeds.append(seed_phrase)
                    
                    # Save to output file
                    with open(output_file, 'a') as f:
                        f.write(f"{seed_phrase}\n")
                else:
                    print("[INFO] Seed has no balance")
                
                # Remove wallet for next iteration
                # Note: You may need to manually manage wallets or restart browser
                # self.remove_wallet()
            else:
                print("[ERROR] Failed to import seed phrase")
            
            # Small delay between iterations
            time.sleep(2)
        
        print(f"\n[COMPLETE] Processed {len(seed_phrases)} seeds")
        print(f"[COMPLETE] Found {len(successful_seeds)} seeds with balance")
        print(f"[COMPLETE] Results saved to: {output_file}")
    
    def cleanup(self):
        """Close browser and cleanup"""
        if self.driver:
            print("[INFO] Closing browser...")
            self.driver.quit()


def main():
    """Main execution function"""
    print("=" * 60)
    print("SafePal Wallet Balance Checker")
    print("=" * 60)
    
    # Initialize automation
    automation = SafePalAutomation()
    
    try:
        # Setup WebDriver
        automation.setup_driver()
        
        print("\n[IMPORTANT] Manual Setup Required:")
        print("1. Install SafePal Extension from Chrome Web Store")
        print("2. Complete initial setup if needed")
        print("3. Press Enter to continue...")
        input()
        
        # Process seed phrases
        automation.process_seed_phrases(VALID_SEEDS_FILE, BALANCE_OUTPUT_FILE)
        
    except KeyboardInterrupt:
        print("\n[INFO] Process interrupted by user")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {str(e)}")
    finally:
        # Cleanup
        automation.cleanup()


if __name__ == "__main__":
    main()
