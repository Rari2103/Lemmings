# -*- coding: utf-8 -*-
"""
Full Trading Agent Demo - Watch it make real trading decisions!
"""
import sys
import logging
from agent import run_agent_demo

# Fix encoding for Windows
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

if __name__ == "__main__":
    print("="*70)
    print(" "*15 + "AI TRADING AGENT - FULL DEMO")
    print(" "*10 + "A Living Agent That Must Trade to Survive")
    print("="*70)
    print("""
This demo runs 5 heartbeat cycles showing:
  - GMAC metabolism (life energy consumption)
  - Real-time market analysis
  - Trading signal generation
  - Position management
  - Survival mechanics

All trades are PAPER TRADES (simulated, no real money)

Press Ctrl+C to stop at any time
    """)
    
    try:
        run_agent_demo(cycles=5)
    except KeyboardInterrupt:
        print("\n\nDemo stopped by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
