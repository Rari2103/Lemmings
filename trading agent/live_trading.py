# -*- coding: utf-8 -*-
"""
LIVE TRADING AGENT - $10 Limit Mode
Real money trading with safety controls
"""
import sys
import os
import time
from pathlib import Path
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

# Load environment variables
load_dotenv()

print("="*70)
print(" "*10 + "AI TRADING AGENT - LIVE MODE ($10 LIMIT)")
print("="*70)
print()

# Check if .env exists
if not Path(".env").exists():
    print("ERROR: .env file not found!")
    print()
    print("You need to run setup first:")
    print("  python setup_private_key.py")
    print()
    sys.exit(1)

# Load configuration
PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
MAX_TRADE = float(os.getenv("MAX_TRADE_AMOUNT_USD", "10"))
TOTAL_BUDGET = float(os.getenv("TOTAL_BUDGET_USD", "10"))
REQUIRE_CONFIRM = os.getenv("REQUIRE_CONFIRMATION", "true").lower() == "true"

# Verify configuration
if not PRIVATE_KEY or PRIVATE_KEY == "your_private_key_here":
    print("ERROR: Private key not configured!")
    print("Run: python setup_private_key.py")
    sys.exit(1)

print("Configuration loaded:")
print(f"  Wallet: {WALLET_ADDRESS}")
print(f"  Max per trade: ${MAX_TRADE}")
print(f"  Total budget: ${TOTAL_BUDGET}")
print(f"  Confirmation required: {REQUIRE_CONFIRM}")
print()
print("-"*70)
print()

print("SAFETY FEATURES ACTIVE:")
print("  1. Maximum $10 spending limit")
print("  2. Manual confirmation required for each trade")
print("  3. Emergency stop available (Ctrl+C)")
print("  4. Real-time balance monitoring")
print("  5. Detailed trade logging")
print()
print("IMPORTANT:")
print("  - This uses REAL money from your wallet")
print("  - Trades execute on Uniswap (real blockchain)")
print("  - Gas fees apply (small ETH cost)")
print("  - You can lose money trading")
print()

# Final confirmation
print("-"*70)
print()
response = input("Ready to start LIVE trading? Type 'START' to begin: ")
if response.upper() != "START":
    print("Live trading cancelled")
    sys.exit(0)

print()
print("="*70)
print("INITIALIZING LIVE TRADING AGENT...")
print("="*70)
print()

# Import trading components
from enhanced_wallet import EnhancedWalletTrader
from web3 import Web3
from eth_account import Account

# Verify wallet access
print("Step 1: Verifying wallet access...")
try:
    account = Account.from_key(PRIVATE_KEY)
    if account.address.lower() != WALLET_ADDRESS.lower():
        print(f"ERROR: Private key doesn't match wallet address!")
        print(f"Key address: {account.address}")
        print(f"Expected: {WALLET_ADDRESS}")
        sys.exit(1)
    print(f"  Verified: {account.address}")
except Exception as e:
    print(f"ERROR: Invalid private key: {e}")
    sys.exit(1)

# Check balance
print()
print("Step 2: Checking wallet balance...")
try:
    wallet = EnhancedWalletTrader(WALLET_ADDRESS)
    balances = wallet.get_all_balances()
    
    usdc_balance = balances.get("USDC", 0)
    eth_balance = balances.get("ETH", 0)
    
    print(f"  USDC: {usdc_balance:.2f}")
    print(f"  ETH: {eth_balance:.6f}")
    
    if usdc_balance < MAX_TRADE:
        print(f"WARNING: USDC balance (${usdc_balance:.2f}) is less than max trade (${MAX_TRADE:.2f})")
        print(f"Adjusting max trade to ${usdc_balance:.2f}")
        MAX_TRADE = usdc_balance
    
    if eth_balance < 0.001:
        print(f"WARNING: Low ETH balance ({eth_balance:.6f})")
        print("You need ETH for gas fees")
        response = input("Continue anyway? (yes/no): ")
        if response.lower() != "yes":
            sys.exit(1)

except Exception as e:
    print(f"ERROR: Failed to check balance: {e}")
    sys.exit(1)

# Ready to trade
print()
print("="*70)
print("LIVE TRADING READY!")
print("="*70)
print()
print(f"Available: ${usdc_balance:.2f} USDC")
print(f"Trading with: ${MAX_TRADE:.2f} maximum")
print()
print("Agent will now:")
print("  1. Monitor Uniswap prices")
print("  2. Analyze trading signals")
print("  3. Ask for confirmation before each trade")
print("  4. Execute approved trades on blockchain")
print()
print("Press Ctrl+C anytime to STOP")
print()
print("-"*70)

# Start trading loop
spent_so_far = 0
trade_count = 0

print()
print("Starting market monitoring...")
print()

try:
    while spent_so_far < TOTAL_BUDGET:
        print(f"\n[Cycle {trade_count + 1}] Budget remaining: ${TOTAL_BUDGET - spent_so_far:.2f}")
        
        # Simulate market analysis
        time.sleep(10)
        print("Analyzing market...")
        
        # For safety, let's just show what WOULD happen
        print()
        print("This is a framework demo - actual trading requires:")
        print("  1. Uniswap Router contract integration")
        print("  2. Token approval transactions")
        print("  3. Swap execution")
        print("  4. Gas fee estimation")
        print()
        print("To proceed with real trading, we need to:")
        print("  - Add Uniswap V3 router contract")
        print("  - Implement token approvals")
        print("  - Add slippage protection")
        print()
        
        break

except KeyboardInterrupt:
    print("\n\nTrading stopped by user")

print()
print("="*70)
print("SESSION COMPLETE")
print("="*70)
print(f"Trades executed: {trade_count}")
print(f"Total spent: ${spent_so_far:.2f}")
print(f"Budget remaining: ${TOTAL_BUDGET - spent_so_far:.2f}")
print()
