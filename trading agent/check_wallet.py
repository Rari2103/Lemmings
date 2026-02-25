# -*- coding: utf-8 -*-
"""
Check Real Wallet Balance - READ ONLY (Safe)
"""
import sys
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

from real_wallet import RealWalletTrader

# Your wallet address
WALLET_ADDRESS = "0x83cc3b8731f6344D7DA6529566D94ACf30271C08"

print("="*70)
print(" "*15 + "CHECKING YOUR REAL WALLET")
print("="*70)
print(f"\nWallet: {WALLET_ADDRESS}")
print("\nConnecting to Ethereum mainnet...")
print("This is READ-ONLY - no transactions will be made")
print()

try:
    # Initialize wallet connection (read-only, no private key)
    wallet = RealWalletTrader(WALLET_ADDRESS)
    
    print("Connected successfully!")
    print(f"Network: Ethereum Mainnet")
    print()
    
    # Get all balances
    print("Fetching balances...")
    balances = wallet.get_all_balances()
    
    print("\n" + "="*70)
    print(" "*20 + "YOUR WALLET BALANCES")
    print("="*70)
    
    if balances:
        total_usd = 0
        for token, amount in balances.items():
            print(f"\n{token}: {amount:.6f}")
            
            # Estimate USD value (approximate)
            if token == "USDC" or token == "USDT":
                usd_value = amount
            elif token == "ETH":
                usd_value = amount * 2500  # Approximate
            elif token == "DAI":
                usd_value = amount
            else:
                usd_value = 0
            
            if usd_value > 0:
                print(f"  ≈ ${usd_value:.2f} USD")
                total_usd += usd_value
        
        print("\n" + "="*70)
        print(f"Total Value: ≈ ${total_usd:.2f} USD")
        print("="*70)
    else:
        print("\nNo balances found")
    
    print(f"\n✅ Your wallet is accessible!")
    print(f"✅ Balance check successful!")
    print()

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
