# Quick Start Guide

## Installation & Setup (5 minutes)

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Install SafePal Extension
- Open Chrome browser
- Visit: https://chromewebstore.google.com/detail/safepal-extension-wallet/lgmpcpglpngdoalbgeoldeajfclnhafa
- Click "Add to Chrome"
- Complete initial setup if prompted

### 3. Prepare Your Seed Phrases
Edit `valid.txt` and add your seed phrases (one per line):
```
abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
test test test test test test test test test test test junk
```

### 4. Run the Script
```bash
# Basic version
python3 safepal_checker.py

# Advanced version (recommended - has better logging)
python3 safepal_checker_advanced.py
```

### 5. Check Results
- Seeds with balance will be saved to `balance.txt`
- Logs are saved to `safepal_checker.log` (advanced version only)

## Two Versions Available

### Basic Version (`safepal_checker.py`)
- Simple and straightforward
- Good for understanding the workflow
- Basic error handling

### Advanced Version (`safepal_checker_advanced.py`) ⭐ RECOMMENDED
- Enhanced error handling
- Detailed logging to file
- Screenshots for debugging
- Multiple detection strategies
- Better UI element detection

## Expected Workflow

1. Script opens Chrome with Selenium
2. For each seed phrase in `valid.txt`:
   - Navigates to SafePal extension
   - Clicks "Add Wallet" → "Import Wallet"
   - Selects "Mnemonic phrase"
   - Enters the seed phrase
   - Clicks "Import"
   - Waits for wallet to load
   - Checks for balance
   - If balance > 0: saves to `balance.txt`
   - Moves to next seed
3. Outputs summary

## Important Notes

### ⚠️ Security Warning
- **NEVER share your seed phrases with anyone**
- Keep `valid.txt` and `balance.txt` secure
- Delete these files after use
- This script is for personal use only

### ⚠️ Limitations
- SafePal UI may change, requiring script updates
- Balance detection may not be 100% accurate
- You may need to manually remove wallets between runs
- Processing many seeds takes time

### 💡 Tips
- Start with 1-2 test seeds to verify it works
- Check the screenshots if balance detection fails
- Review the log file for detailed information
- Manually verify any seeds marked as having balance

## Troubleshooting

### Script can't find buttons
**Problem**: XPath selectors don't match SafePal UI

**Solution**: 
1. Open Chrome DevTools (F12)
2. Inspect the button elements
3. Update the XPath in the script

### Balance not detected
**Problem**: Script reports no balance but wallet has funds

**Solution**:
1. Check the screenshots in the script directory
2. Increase `BALANCE_CHECK_WAIT` in the script
3. Manually verify the balance in SafePal
4. Update balance detection logic if needed

### Extension not loading
**Problem**: Script can't access SafePal extension

**Solution**:
1. Verify extension is installed
2. Check extension ID is correct: `lgmpcpglpngdoalbgeoldeajfclnhafa`
3. Try manually opening: `chrome-extension://lgmpcpglpngdoalbgeoldeajfclnhafa/index.html`

## File Structure
```
safepal_automation/
├── safepal_checker.py              # Basic version
├── safepal_checker_advanced.py     # Advanced version ⭐
├── valid.txt                       # INPUT: Your seed phrases
├── balance.txt                     # OUTPUT: Seeds with balance
├── safepal_checker.log            # OUTPUT: Detailed logs
├── requirements.txt                # Python dependencies
├── README.md                       # Full documentation
└── QUICKSTART.md                   # This file
```

## Next Steps

1. Test with a known seed phrase first
2. Review the logs and screenshots
3. Adjust wait times if needed
4. Process your actual seed phrases
5. Manually verify any positive results
6. Securely delete sensitive files when done

## Support

For SafePal-specific issues: https://www.safepal.com/support

For script issues: Review the code and logs, update selectors as needed.

---

**Good luck and stay safe! 🔐**
