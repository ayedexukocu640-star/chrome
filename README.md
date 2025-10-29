# SafePal Wallet Balance Checker

This Python script automates the process of checking balances for multiple seed phrases using the SafePal Chrome extension and Selenium WebDriver.

## Overview

The script reads seed phrases from a text file, imports each one into the SafePal wallet extension, checks the balance, and saves only the seed phrases that have a non-zero balance to an output file.

## Features

- Automated seed phrase import into SafePal wallet
- Balance checking for each imported wallet
- Saves only seeds with balances to output file
- Error handling and logging
- Support for 12, 18, and 24-word seed phrases

## Requirements

### Software Requirements
- Python 3.7 or higher
- Google Chrome browser
- SafePal Extension Wallet (Chrome extension)

### Python Dependencies
- selenium
- webdriver-manager

## Installation

### Step 1: Install Python Dependencies

```bash
pip3 install selenium webdriver-manager
```

### Step 2: Install SafePal Extension

1. Open Google Chrome
2. Visit the Chrome Web Store: https://chromewebstore.google.com/detail/safepal-extension-wallet/lgmpcpglpngdoalbgeoldeajfclnhafa
3. Click "Add to Chrome" to install the SafePal Extension Wallet
4. Complete the initial setup if prompted

### Step 3: Prepare Input File

Create a file named `valid.txt` in the same directory as the script, with one seed phrase per line:

```
abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
test test test test test test test test test test test junk
your seed phrase goes here with words separated by spaces
```

## Usage

### Basic Usage

```bash
python3 safepal_checker.py
```

### What the Script Does

1. Opens Chrome with Selenium WebDriver
2. Navigates to the SafePal extension
3. For each seed phrase in `valid.txt`:
   - Imports the seed phrase into SafePal wallet
   - Waits for the wallet to load
   - Checks the balance
   - If balance > 0, saves the seed phrase to `balance.txt`
   - Prepares for the next seed phrase
4. Outputs results to `balance.txt`

## File Structure

```
safepal_automation/
├── safepal_checker.py    # Main script
├── valid.txt             # Input file with seed phrases (one per line)
├── balance.txt           # Output file with seeds that have balance
└── README.md             # This file
```

## Configuration

You can modify these variables in the script:

```python
EXTENSION_ID = "lgmpcpglpngdoalbgeoldeajfclnhafa"  # SafePal extension ID
VALID_SEEDS_FILE = "valid.txt"                     # Input file name
BALANCE_OUTPUT_FILE = "balance.txt"                # Output file name
WAIT_TIMEOUT = 30                                  # Timeout in seconds
```

## Important Notes

### Security Warning
**NEVER share your seed phrases with anyone!** This script is for educational and personal use only. Keep your seed phrases secure and private.

### Limitations

1. **Manual Setup Required**: The SafePal extension must be installed manually in Chrome before running the script
2. **UI Dependencies**: The script relies on the SafePal extension's UI elements, which may change with updates
3. **Rate Limiting**: Processing many seed phrases may take time due to blockchain data loading
4. **Wallet Management**: You may need to manually remove wallets between imports or restart the browser periodically

### Troubleshooting

**Problem**: Script cannot find SafePal extension
- **Solution**: Make sure the extension is installed and the extension ID is correct

**Problem**: Script fails to click buttons
- **Solution**: The SafePal UI may have changed. You'll need to update the XPath selectors in the script

**Problem**: Balance not detected
- **Solution**: Increase the wait time or check the balance display elements in SafePal's UI

**Problem**: Too many wallets imported
- **Solution**: Manually remove wallets from SafePal extension or implement wallet removal logic

## Customization

### Updating UI Selectors

If the SafePal extension UI changes, you may need to update the XPath selectors in these methods:

- `import_seed_phrase()`: Buttons for "Add Wallet", "Import Wallet", "Mnemonic phrase"
- `check_balance()`: Balance display elements

To find the correct selectors:
1. Open Chrome DevTools (F12)
2. Use the element inspector to find the correct elements
3. Update the XPath expressions in the script

### Adding Balance Detection Logic

The current balance detection is basic. You can enhance it by:

1. Checking specific cryptocurrency balances (BTC, ETH, etc.)
2. Adding support for multiple chains
3. Implementing more robust balance parsing

## Example Output

**Console Output:**
```
============================================================
SafePal Wallet Balance Checker
============================================================
[INFO] Chrome WebDriver initialized successfully
[INFO] Found 3 seed phrases to process

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

**balance.txt Output:**
```
test test test test test test test test test test test junk
```

## Disclaimer

This script is provided for educational purposes only. Use at your own risk. The authors are not responsible for any loss of funds or other damages resulting from the use of this script.

Always verify balances through official wallet applications and never share your seed phrases with anyone.

## License

This script is provided as-is without any warranty. Feel free to modify and use it for personal purposes.

## Support

For issues with:
- **SafePal Extension**: Visit https://www.safepal.com/support
- **This Script**: Check the code comments and update selectors as needed

## Version History

- **v1.0** (2025-10-29): Initial release
  - Basic seed phrase import
  - Balance checking
  - Output to file
