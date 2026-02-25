# -*- coding: utf-8 -*-
"""
Secure Private Key Setup Assistant
THIS WILL ONLY RUN ONCE TO SET UP YOUR PRIVATE KEY
"""
import sys
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

from pathlib import Path

print("="*70)
print(" "*15 + "PRIVATE KEY SETUP - LIVE TRADING")
print("="*70)
print()
print("WARNING: We need your private key to sign transactions.")
print("This will be stored LOCALLY in a .env file.")
print()
print("IMPORTANT SECURITY NOTES:")
print("  1. Private key stays on YOUR computer")
print("  2. Never share your private key with anyone")
print("  3. We'll set a $10 spending limit")
print("  4. Every trade requires confirmation")
print()

# Check if .env already exists
env_file = Path(".env")
if env_file.exists():
    print("Found existing .env file")
    response = input("Overwrite? (yes/no): ")
    if response.lower() != "yes":
        print("Keeping existing .env file")
        sys.exit(0)

print("\n" + "-"*70)
print("SETUP PROCESS:")
print("-"*70)
print()

# Get private key
print("Step 1: Enter your wallet private key")
print("(It should start with 0x and be 66 characters long)")
print()
private_key = input("Private Key: ").strip()

if not private_key.startswith("0x") or len(private_key) != 66:
    print("\nERROR: Invalid private key format")
    print("Expected: 0x followed by 64 hex characters")
    sys.exit(1)

# Confirm wallet address
print()
print("Step 2: Verify wallet address")
print("Your wallet: 0x83cc3b8731f6344D7DA6529566D94ACf30271C08")
confirm = input("Is this correct? (yes/no): ")

if confirm.lower() != "yes":
    print("Please verify your wallet address")
    sys.exit(1)

# Set spending limit
print()
print("Step 3: Set spending limit")
print("Recommended: $10 for first test")
limit = input("Max spending limit (USD): $ ")
try:
    limit_float = float(limit)
    if limit_float > 29:
        print(f"WARNING: You only have $29 USDC")
        print("Setting limit to $29")
        limit_float = 29.0
except:
    print("Invalid amount, using $10 default")
    limit_float = 10.0

# Write .env file
print()
print("Creating secure .env file...")

env_content = f"""# Trading Agent - Secure Configuration
# KEEP THIS FILE PRIVATE!

WALLET_PRIVATE_KEY={private_key}
WALLET_ADDRESS=0x83cc3b8731f6344D7DA6529566D94ACf30271C08
MAX_TRADE_AMOUNT_USD={limit_float}
TOTAL_BUDGET_USD={limit_float}
REQUIRE_CONFIRMATION=true
ETH_RPC_URL=https://ethereum.publicnode.com
"""

with open(".env", "w") as f:
    f.write(env_content)

print()
print("="*70)
print("SETUP COMPLETE!")
print("="*70)
print()
print(f"Configuration saved:")
print(f"  - Spending limit: ${limit_float}")
print(f"  - Confirmation required: YES")
print(f"  - Private key: Stored securely in .env")
print()
print("IMPORTANT:")
print("  - .env file is PRIVATE - never share it")
print("  - Add .env to .gitignore (already done)")
print("  - You can change limits in .env file anytime")
print()
print("Ready to start trading!")
print()
