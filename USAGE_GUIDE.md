# SafePal Wallet Balance Checker - Usage Guide

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Script](#running-the-script)
5. [Understanding the Output](#understanding-the-output)
6. [Customization](#customization)
7. [Troubleshooting](#troubleshooting)
8. [Security Best Practices](#security-best-practices)

## Overview

This tool automates the process of checking balances for multiple cryptocurrency wallet seed phrases using the SafePal browser extension. It's designed for users who need to check many seed phrases efficiently.

### How It Works

The script uses Selenium WebDriver to control Chrome browser and interact with the SafePal extension. For each seed phrase:

1. Opens SafePal extension
2. Imports the seed phrase
3. Waits for wallet to load
4. Checks for any balance
5. Saves seed phrases with non-zero balances
6. Moves to the next seed phrase

## Installation

### Prerequisites

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.7 or higher
- **Chrome Browser**: Latest version recommended
- **Internet Connection**: Required for blockchain data

### Step-by-Step Installation

#### 1. Install Python Dependencies

```bash
# Navigate to the project directory
cd safepal_automation

# Install required packages
pip3 install -r requirements.txt
```

Or install manually:
```bash
pip3 install selenium webdriver-manager
```

#### 2. Install SafePal Extension

1. Open Google Chrome
2. Visit the Chrome Web Store: https://chromewebstore.google.com/detail/safepal-extension-wallet/lgmpcpglpngdoalbgeoldeajfclnhafa
3. Click **"Add to Chrome"**
4. Click **"Add extension"** in the popup
5. The SafePal icon should appear in your Chrome toolbar

#### 3. Verify Installation

Run the test script to verify everything is set up correctly:

```bash
python3 test_setup.py
```

Expected output:
```
Testing Selenium and Chrome setup...
--------------------------------------------------
✓ Chrome options configured
✓ Chrome WebDriver initialized successfully
✓ Successfully navigated to: https://www.google.com
✓ SafePal extension appears to be accessible
✓ Browser closed successfully
```

## Configuration

### Input File: `valid.txt`

This file contains the seed phrases you want to check. Format:

```
abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
test test test test test test test test test test test junk
your actual seed phrase goes here with words separated by spaces
```

**Important:**
- One seed phrase per line
- Words separated by single spaces
- Supports 12, 18, or 24-word seed phrases
- No empty lines between seed phrases

### Script Configuration

You can modify these settings in the script files:

```python
# In safepal_checker.py or safepal_checker_advanced.py

EXTENSION_ID = "lgmpcpglpngdoalbgeoldeajfclnhafa"  # SafePal extension ID
VALID_SEEDS_FILE = "valid.txt"                     # Input file
BALANCE_OUTPUT_FILE = "balance.txt"                # Output file
WAIT_TIMEOUT = 30                                  # Max wait time (seconds)
BALANCE_CHECK_WAIT = 10                            # Balance load time (seconds)
```

## Running the Script

### Option 1: Basic Version

```bash
python3 safepal_checker.py
```

**When to use:**
- First time testing
- Simple use case
- Don't need detailed logs

### Option 2: Advanced Version (Recommended)

```bash
python3 safepal_checker_advanced.py
```

**When to use:**
- Processing many seed phrases
- Need detailed logging
- Want screenshots for debugging
- Better error handling needed

### Interactive Process

When you run the script, you'll see:

```
============================================================
SafePal Wallet Balance Checker - Advanced Version
============================================================
[INFO] Chrome WebDriver initialized successfully

============================================================
IMPORTANT: Manual Setup Required
============================================================
1. Install SafePal Extension from Chrome Web Store
2. Complete initial setup if needed
3. Make sure valid.txt contains your seed phrases
4. Press Enter to start processing...
============================================================
```

**Press Enter** when ready to start processing.

### What Happens Next

The script will:

1. Open Chrome browser (controlled by Selenium)
2. Navigate to SafePal extension
3. Process each seed phrase automatically
4. Display progress in the console
5. Save results to `balance.txt`
6. Close the browser when complete

## Understanding the Output

### Console Output

**Basic Version:**
```
[INFO] Processing seed 1/3
[INFO] Importing seed phrase: abandon abandon aban...
[INFO] Seed phrase imported successfully
[INFO] Checking wallet balance...
[INFO] No balance found or balance is 0

[INFO] Processing seed 2/3
[INFO] Importing seed phrase: test test test test...
[INFO] Seed phrase imported successfully
[INFO] Checking wallet balance...
[SUCCESS] Balance found: 0.5
[SUCCESS] Seed has balance: 0.5

[COMPLETE] Processed 3 seeds
[COMPLETE] Found 1 seeds with balance
[COMPLETE] Results saved to: balance.txt
```

**Advanced Version:**
```
2025-10-29 17:00:00 - INFO - Processing seed 1/3
2025-10-29 17:00:05 - INFO - Importing seed phrase: abandon abandon aban...
2025-10-29 17:00:10 - INFO - Seed phrase imported successfully
2025-10-29 17:00:15 - INFO - Checking wallet balance...
2025-10-29 17:00:25 - INFO - ✗ Seed has no balance

2025-10-29 17:00:30 - INFO - Processing seed 2/3
2025-10-29 17:00:35 - INFO - Importing seed phrase: test test test test...
2025-10-29 17:00:40 - INFO - Seed phrase imported successfully
2025-10-29 17:00:45 - INFO - Checking wallet balance...
2025-10-29 17:00:55 - INFO - ✓ Seed has balance: 0.5
```

### Output Files

#### `balance.txt`
Contains only seed phrases that have non-zero balances:

```
test test test test test test test test test test test junk
another seed phrase with balance goes here
```

#### `safepal_checker.log` (Advanced version only)
Detailed log file with timestamps and debug information:

```
2025-10-29 17:00:00,123 - INFO - Chrome WebDriver initialized successfully
2025-10-29 17:00:05,456 - INFO - Found 3 seed phrases to process
2025-10-29 17:00:10,789 - INFO - Processing seed 1/3
...
```

#### Screenshots (Advanced version only)
Saved as PNG files with timestamps:
- `balance_check_20251029_170000.png` - Screenshot during balance check
- `error_add_wallet_20251029_170100.png` - Error screenshots for debugging

## Customization

### Adjusting Wait Times

If the script is too fast or too slow, adjust these values:

```python
# Increase if wallet loads slowly
BALANCE_CHECK_WAIT = 15  # Default: 10 seconds

# Increase if elements take time to appear
WAIT_TIMEOUT = 45  # Default: 30 seconds
```

### Customizing Balance Detection

The advanced version uses multiple strategies to detect balances. You can add more:

```python
def check_balance(self):
    # Strategy 4: Check specific token balances
    try:
        usdt_elements = self.driver.find_elements(By.XPATH, 
            "//*[contains(text(), 'USDT')]"
        )
        for element in usdt_elements:
            # Your custom logic here
            pass
    except Exception as e:
        logger.debug(f"Strategy 4 failed: {str(e)}")
```

### Adding Support for More Cryptocurrencies

Modify the balance checking logic to look for specific tokens:

```python
# In check_balance() method
crypto_elements = self.driver.find_elements(By.XPATH,
    "//*[contains(text(), 'BTC')] | "
    "//*[contains(text(), 'ETH')] | "
    "//*[contains(text(), 'BNB')] | "
    "//*[contains(text(), 'USDT')] | "  # Add more tokens
    "//*[contains(text(), 'SOL')]"      # Add more tokens
)
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Extension Not Found

**Error:**
```
[ERROR] Failed to open extension: ERR_FILE_NOT_FOUND
```

**Solution:**
- Verify SafePal extension is installed in Chrome
- Check the extension ID is correct: `lgmpcpglpngdoalbgeoldeajfclnhafa`
- Try manually opening: `chrome-extension://lgmpcpglpngdoalbgeoldeajfclnhafa/index.html`

#### 2. Buttons Not Clickable

**Error:**
```
[WARNING] Timeout waiting for Add Wallet button
```

**Solution:**
- SafePal UI may have changed
- Open Chrome DevTools (F12) and inspect the button
- Update the XPath selector in the script:

```python
# Find the correct XPath
add_wallet_selectors = [
    "//button[contains(text(), 'Add Wallet')]",  # Update this
    "//div[contains(text(), 'Add Wallet')]",     # Or this
]
```

#### 3. Balance Not Detected

**Error:**
```
[INFO] No balance found or balance is 0
```

**Solution:**
- Check the screenshots to see what the script sees
- Increase `BALANCE_CHECK_WAIT` to allow more loading time
- Manually verify the balance in SafePal
- Update balance detection XPath selectors

#### 4. Chrome Driver Issues

**Error:**
```
selenium.common.exceptions.WebDriverException
```

**Solution:**
```bash
# Update Chrome to latest version
# Reinstall selenium
pip3 uninstall selenium
pip3 install selenium webdriver-manager
```

#### 5. Too Many Wallets

**Problem:** SafePal has too many imported wallets

**Solution:**
- Manually remove wallets from SafePal extension
- Or use a fresh Chrome profile:

```python
automation = SafePalAdvancedAutomation(
    chrome_profile_path="/path/to/fresh/profile"
)
```

### Debug Mode

Enable more detailed logging:

```python
# In the script, change logging level
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO
    ...
)
```

### Manual Verification

Always manually verify seeds marked as having balance:

1. Open SafePal extension manually
2. Import the seed phrase
3. Check actual balance
4. Compare with script results

## Security Best Practices

### Before Running

1. **Verify Script Source**: Review the code before running
2. **Test Environment**: Use a test seed phrase first
3. **Backup**: Keep secure backups of important seed phrases
4. **Antivirus**: Ensure your system is clean

### During Operation

1. **Private Network**: Use a secure, private internet connection
2. **No Screen Sharing**: Don't share your screen while running
3. **Monitor Activity**: Watch the browser automation carefully
4. **Limit Access**: Don't let others access your computer

### After Running

1. **Delete Sensitive Files**:
```bash
# Securely delete files
rm valid.txt
rm balance.txt
rm safepal_checker.log
rm *.png  # Delete screenshots
```

2. **Clear Browser Data**: Clear Chrome history and cache
3. **Remove Wallets**: Delete imported wallets from SafePal
4. **Secure Storage**: Store results in encrypted storage

### General Security

⚠️ **CRITICAL WARNINGS:**

- **NEVER share your seed phrases** with anyone
- **NEVER upload seed phrases** to cloud services
- **NEVER run this script** on untrusted computers
- **NEVER leave files** with seed phrases unencrypted
- **ALWAYS verify** balances manually before taking action
- **ALWAYS use** this tool on a secure, private computer

### Recommended Workflow

1. Test with a known test seed phrase
2. Process a small batch (5-10 seeds)
3. Manually verify results
4. Process remaining seeds in batches
5. Immediately secure any seeds with balances
6. Delete all temporary files
7. Clear browser data

## Advanced Usage

### Using Custom Chrome Profile

```python
# Create a dedicated Chrome profile for this task
automation = SafePalAdvancedAutomation(
    chrome_profile_path="/home/user/.config/google-chrome/SafePal"
)
```

### Batch Processing

Process seeds in batches to avoid issues:

```python
# Split valid.txt into smaller files
# valid_batch1.txt, valid_batch2.txt, etc.

# Process each batch separately
automation.process_seed_phrases("valid_batch1.txt", "balance_batch1.txt")
```

### Headless Mode (Not Recommended)

For advanced users only - makes debugging harder:

```python
chrome_options.add_argument('--headless')
```

## Support and Resources

### SafePal Resources
- Official Website: https://www.safepal.com
- Support: https://www.safepal.com/support
- Documentation: https://docs.safepal.io

### Selenium Resources
- Documentation: https://selenium-python.readthedocs.io
- Troubleshooting: https://www.selenium.dev/documentation/

### Script Support
- Review the code and comments
- Check log files for detailed errors
- Take screenshots for visual debugging
- Update XPath selectors as needed

---

**Remember: Always prioritize security when handling seed phrases!** 🔐
