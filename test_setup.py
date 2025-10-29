#!/usr/bin/env python3
"""
Test script to verify Selenium and Chrome setup
"""

import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_selenium_setup():
    """Test if Selenium and Chrome are working"""
    print("Testing Selenium and Chrome setup...")
    print("-" * 50)
    
    try:
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        print("✓ Chrome options configured")
        
        # Initialize driver
        print("Initializing Chrome WebDriver...")
        driver = webdriver.Chrome(options=chrome_options)
        print("✓ Chrome WebDriver initialized successfully")
        
        # Test navigation
        print("Testing navigation...")
        driver.get("https://www.google.com")
        print(f"✓ Successfully navigated to: {driver.current_url}")
        print(f"✓ Page title: {driver.title}")
        
        # Test SafePal extension URL (will fail if not installed, which is expected)
        print("\nTesting SafePal extension access...")
        extension_id = "lgmpcpglpngdoalbgeoldeajfclnhafa"
        extension_url = f"chrome-extension://{extension_id}/index.html"
        
        driver.get(extension_url)
        print(f"✓ Navigated to extension URL: {extension_url}")
        
        # Check if extension is installed
        if "chrome-extension" in driver.current_url:
            print("✓ SafePal extension appears to be accessible")
            print(f"  Current URL: {driver.current_url}")
        else:
            print("⚠ SafePal extension may not be installed")
            print("  Please install from Chrome Web Store")
        
        # Cleanup
        driver.quit()
        print("\n✓ Browser closed successfully")
        
        print("\n" + "=" * 50)
        print("SETUP TEST COMPLETE")
        print("=" * 50)
        print("✓ Selenium is working correctly")
        print("✓ Chrome WebDriver is functional")
        print("\nNext steps:")
        print("1. Install SafePal extension if not already installed")
        print("2. Add seed phrases to valid.txt")
        print("3. Run safepal_checker_advanced.py")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error during setup test: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure Chrome is installed")
        print("2. Install dependencies: pip3 install selenium webdriver-manager")
        print("3. Check Chrome version compatibility")
        return False


if __name__ == "__main__":
    success = test_selenium_setup()
    sys.exit(0 if success else 1)
