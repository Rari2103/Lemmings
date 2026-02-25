# -*- coding: utf-8 -*-
"""
Extended Trading Demo - Run longer to catch real trades
"""
import sys
import logging
import time
from agent import TradingAgent

sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    print("="*70)
    print(" "*15 + "AI TRADING AGENT - LIVE SESSION")
    print("="*70)
    print("""
This runs the agent continuously showing:
  [*] Real market analysis every 30 seconds
  [*] GMAC consumption in real-time
  [*] Trading signals when detected
  [*] Automatic trade execution
  [*] Survival mechanics

PAPER TRADING MODE - No real money at risk

Will run 15 cycles (~7.5 minutes). Press Ctrl+C to stop early.
    """)
    
    agent = TradingAgent("Trader-Alpha")
    
    cycles = 15
    cycle_interval = 30  # seconds
    
    try:
        for i in range(cycles):
            print(f"\n{'*'*70}")
            print(f" Cycle {i+1}/{cycles} - {time.strftime('%H:%M:%S')}")
            print('*'*70)
            
            if not agent.heartbeat():
                logger.error("Agent has died!")
                break
            
            # Show current status
            print(f"\n>>> Status: GMAC={agent.gmac:.1f} | "
                  f"Goodwill={agent.goodwill} | "
                  f"Trades={agent.trades_executed}")
            
            if agent.survival_mode:
                print(">>> MODE: SURVIVAL (conserving energy)")
            elif agent.critical_mode:
                print(">>> MODE: CRITICAL (minimal operations)")
            
            if i < cycles - 1:
                print(f"\nNext heartbeat in {cycle_interval} seconds...")
                time.sleep(cycle_interval)
        
        # Final report
        print("\n" + "="*70)
        print(" "*20 + "SESSION COMPLETE")
        print("="*70)
        print(f"\nAgent Name: {agent.name}")
        print(f"Status: {'ALIVE' if agent.alive else 'DEAD'}")
        print(f"Final GMAC: {agent.gmac:.2f}")
        print(f"Final Goodwill: {agent.goodwill}")
        print(f"Total Heartbeats: {agent.heartbeats}")
        print(f"Trades Executed: {agent.trades_executed}")
        print(f"Win/Loss: {agent.winning_trades}/{agent.losing_trades}")
        print(f"Total P&L: ${agent.total_pnl:.2f}")
        print(f"\nFinal Balance:")
        for currency, amount in agent.trader.get_balance().items():
            if amount > 0.0001:
                print(f"  {currency}: {amount:.6f}")
        print()
        
    except KeyboardInterrupt:
        print("\n\nSession interrupted by user")
        print(f"\nQuick Stats:")
        print(f"  GMAC: {agent.gmac:.2f}")
        print(f"  Trades: {agent.trades_executed}")
        print(f"  Balance: {agent.trader.get_balance()}")
