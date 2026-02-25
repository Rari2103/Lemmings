# -*- coding: utf-8 -*-
"""
DEMO MODE - Shows trading with guaranteed signals
"""
import sys
import time
import logging
import random

sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class DemoTrader:
    """Demo trader that always finds trading opportunities"""
    
    def __init__(self):
        self.balance = {"USDT": 1000.0, "ETH": 0.0}
        self.trades = []
    
    def get_balance(self):
        return self.balance.copy()
    
    def execute_trade(self, symbol, side, amount, price):
        """Execute a simulated trade"""
        if side == "BUY":
            cost = amount * price
            if self.balance["USDT"] >= cost:
                self.balance["USDT"] -= cost
                self.balance["ETH"] = self.balance.get("ETH", 0) + amount
                self.trades.append({
                    "side": "BUY",
                    "amount": amount,
                    "price": price,
                    "cost": cost
                })
                return True
        elif side == "SELL":
            if self.balance.get("ETH", 0) >= amount:
                self.balance["ETH"] -= amount
                revenue = amount * price
                self.balance["USDT"] += revenue
                self.trades.append({
                    "side": "SELL",
                    "amount": amount,
                    "price": price,
                    "revenue": revenue
                })
                return True
        return False


def run_demo_with_guaranteed_trade():
    """Demo that guarantees showing a trade"""
    print("\n" + "="*70)
    print(" "*15 + "AI TRADING AGENT - GUARANTEED TRADE DEMO")
    print("="*70)
    print("\nThis demo will DEFINITELY execute a trade to show you how it works!")
    print("All trades are simulated (paper trading)")
    print()
    
    trader = DemoTrader()
    gmac = 1000.0
    
    # Show initial state
    print(f"Initial Balance: ${trader.balance['USDT']:.2f} USDT")
    print(f"Initial GMAC: {gmac:.1f}")
    print()
    
    # Simulate market analysis
    for cycle in range(1, 4):
        print(f"\n{'='*70}")
        print(f"CYCLE {cycle}")
        print('='*70)
        
        gmac -= 1.5  # Heartbeat cost
        print(f"GMAC: {gmac:.1f}")
        
        # Generate a trading signal
        eth_price = 2500 + random.randint(-50, 50)
        print(f"\nETH Price: ${eth_price:.2f}")
        print("Analyzing market...")
        time.sleep(1)
        
        if cycle == 2:  # Make the trade on cycle 2
            print("\n*** STRONG BUY SIGNAL DETECTED! ***")
            print(f"RSI: 25 (Oversold)")
            print(f"MA Crossover: Bullish")
            print(f"Confidence: 85%")
            
            # Calculate position size
            position_size = trader.balance["USDT"] * 0.25  # 25% of balance
            eth_amount = position_size / eth_price
            
            print(f"\nExecuting Trade:")
            print(f"  Action: BUY")
            print(f"  Amount: {eth_amount:.6f} ETH")
            print(f"  Price: ${eth_price:.2f}")
            print(f"  Cost: ${position_size:.2f} USDT")
            
            gmac -= 2.0  # Trade execution cost
            
            if trader.execute_trade("ETH/USDT", "BUY", eth_amount, eth_price):
                gmac += 50  # Earn GMAC for successful trade
                print(f"\n*** TRADE EXECUTED SUCCESSFULLY! ***")
                print(f"GMAC earned: +50 (Total: {gmac:.1f})")
                print(f"\nNew Balance:")
                print(f"  USDT: ${trader.balance['USDT']:.2f}")
                print(f"  ETH: {trader.balance['ETH']:.6f}")
                break
        else:
            print("No strong signal - waiting...")
        
        time.sleep(2)
    
    # Summary
    print(f"\n{'='*70}")
    print(" "*25 + "DEMO COMPLETE!")
    print('='*70)
    print(f"\nTotal Cycles: {cycle}")
    print(f"Final GMAC: {gmac:.1f}")
    print(f"Trades Executed: {len(trader.trades)}")
    print(f"\nFinal Balance:")
    print(f"  USDT: ${trader.balance['USDT']:.2f}")
    print(f"  ETH: {trader.balance['ETH']:.6f}")
    
    if trader.trades:
        print(f"\nTrade Details:")
        for i, trade in enumerate(trader.trades, 1):
            print(f"  {i}. {trade['side']} {trade['amount']:.6f} ETH @ ${trade['price']:.2f}")
            if trade['side'] == "BUY":
                print(f"     Cost: ${trade['cost']:.2f} USDT")
            else:
                print(f"     Revenue: ${trade['revenue']:.2f} USDT")
    
    print(f"\n{'='*70}")
    print("This shows exactly how the agent:")
    print("  1. Consumes GMAC energy each cycle")
    print("  2. Analyzes market conditions")
    print("  3. Detects trading signals")
    print("  4. Executes trades when confident")
    print("  5. Earns GMAC from successful trades")
    print('='*70)
    print()


if __name__ == "__main__":
    run_demo_with_guaranteed_trade()
