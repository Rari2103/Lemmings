# -*- coding: utf-8 -*-
"""
Aggressive Uniswap Trading Agent - Trades more frequently
"""
import sys
import time
import logging
from uniswap_trading import UniswapTrader
from strategy import get_strategy
from config import *

sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)


class AggressiveAgent:
    """Aggressive trading agent for Uniswap"""
    
    def __init__(self, name: str = "Uniswap-Trader"):
        self.name = name
        self.gmac = INITIAL_GMAC
        self.goodwill = INITIAL_GOODWILL
        self.alive = True
        self.survival_mode = False
        self.critical_mode = False
        
        # Use Uniswap trader
        self.trader = UniswapTrader()
        self.strategy = get_strategy(STRATEGY_TYPE)
        
        # Statistics
        self.heartbeats = 0
        self.trades_executed = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_pnl = 0.0
        self.positions = []
        
        logger.info(f"Agent {self.name} initialized | GMAC: {self.gmac} | Platform: Uniswap")
    
    def heartbeat(self) -> bool:
        """Process one heartbeat - more aggressive trading"""
        if not self.alive:
            return False
        
        self.heartbeats += 1
        self.gmac -= GMAC_HEARTBEAT_COST
        
        print(f"\n{'='*70}")
        print(f"HEARTBEAT #{self.heartbeats} - {self.name}")
        print(f"GMAC: {self.gmac:.1f} | Goodwill: {self.goodwill} | Trades: {self.trades_executed}")
        print('='*70)
        
        # Check survival
        self._check_survival()
        if not self.alive:
            return False
        
        # Fetch market data
        print("Fetching Uniswap market data...")
        market_data = self.trader.get_market_data(TRADING_PAIRS)
        self.gmac -= GMAC_API_CALL_COST * len(TRADING_PAIRS)
        
        # Analyze (aggressive - lower threshold)
        if not self.critical_mode and market_data:
            self.gmac -= GMAC_INFERENCE_BASE_COST
            signal = self.strategy.analyze(market_data)
            
            if signal.get("action") != "HOLD":
                confidence = signal.get("confidence", 0)
                threshold = 0.50  # LOWER threshold (was 0.70)
                
                if self.survival_mode:
                    threshold = 0.65
                
                print(f"\nSignal: {signal['action']} {signal.get('symbol')}")
                print(f"Confidence: {confidence:.1%} | Threshold: {threshold:.1%}")
                
                if confidence >= threshold:
                    self._execute_trade(signal)
                else:
                    print(f"Signal too weak - need {threshold:.1%}, got {confidence:.1%}")
            else:
                print("No trade signal")
        
        return True
    
    def _check_survival(self):
        """Check survival status"""
        if self.gmac <= GMAC_DEATH_THRESHOLD:
            self.alive = False
            print(f"\n!!! AGENT DIED - GMAC depleted !!!")
            return
        
        if self.gmac <= GMAC_CRITICAL_THRESHOLD:
            if not self.critical_mode:
                self.critical_mode = True
                print(f"\n!!! CRITICAL MODE - GMAC: {self.gmac:.1f} !!!")
        elif self.gmac <= GMAC_SURVIVAL_THRESHOLD:
            if not self.survival_mode:
                self.survival_mode = True
                print(f"\n!!! SURVIVAL MODE - GMAC: {self.gmac:.1f} !!!")
        else:
            self.survival_mode = False
            self.critical_mode = False
    
    def _execute_trade(self, signal: Dict):
        """Execute trade aggressively"""
        self.gmac -= GMAC_TRADE_COST
        
        symbol = signal["symbol"]
        side = signal["action"]
        price = signal["price"]
        
        # Get balance
        balance = self.trader.get_balance()
        quote_currency = symbol.split("_")[1]
        available = balance.get(quote_currency, 0)
        
        # Position sizing
        position_pct = MAX_POSITION_SIZE
        if self.survival_mode:
            position_pct = SURVIVAL_MODE_POSITION_SIZE
        
        trade_amount = available * position_pct
        quantity = trade_amount / price if price > 0 else 0
        
        print(f"\nExecuting: {side} {quantity:.6f} {symbol} @ ${price:.2f}")
        print(f"Trade value: ${trade_amount:.2f}")
        
        # Execute
        result = self.trader.place_order(symbol, side, "MARKET", quantity, price)
        
        if result.get("success"):
            self.trades_executed += 1
            self.goodwill += GOODWILL_TASK_COMPLETE
            
            print(f"SUCCESS! Trade #{self.trades_executed}")
            print(f"Goodwill: {self.goodwill} (+{GOODWILL_TASK_COMPLETE})")
            print(f"New balance: {self.trader.get_balance()}")
            
            # Track position
            self.positions.append({
                "symbol": symbol,
                "side": side,
                "price": price,
                "quantity": quantity,
                "time": time.time()
            })
        else:
            print(f"FAILED: {result.get('error')}")


def run_aggressive_demo():
    """Run aggressive trading demo"""
    print("\n" + "="*70)
    print(" "*15 + "AGGRESSIVE UNISWAP TRADING AGENT")
    print(" "*20 + "Lower confidence threshold")
    print(" "*25 + "More trades!")
    print("="*70)
    
    agent = AggressiveAgent("Uniswap-Alpha")
    
    print("\nTrading on Uniswap DEX")
    print("Pairs: WETH/USDT, WETH/USDC, USDC/USDT")
    print("Mode: PAPER TRADING (simulated)")
    print("Confidence threshold: 50% (aggressive!)")
    print("\nRunning until we make a trade...")
    print("Press Ctrl+C to stop\n")
    
    cycles = 0
    max_cycles = 20  # Safety limit
    
    try:
        while agent.trades_executed == 0 and cycles < max_cycles:
            cycles += 1
            print(f"\n[Cycle {cycles}] Searching for trade opportunity...")
            
            if not agent.heartbeat():
                break
            
            if agent.trades_executed > 0:
                print(f"\n{'*'*70}")
                print(" "*20 + "TRADE EXECUTED!")
                print('*'*70)
                break
            
            # Wait before next cycle
            time.sleep(5)
        
        # Summary
        print("\n" + "="*70)
        print(" "*25 + "DEMO COMPLETE")
        print("="*70)
        print(f"\nAgent: {agent.name}")
        print(f"Heartbeats: {agent.heartbeats}")
        print(f"GMAC: {agent.gmac:.2f}")
        print(f"Goodwill: {agent.goodwill}")
        print(f"Trades: {agent.trades_executed}")
        print(f"\nFinal Balance:")
        for curr, amt in agent.trader.get_balance().items():
            if amt > 0.0001:
                print(f"  {curr}: {amt:.6f}")
        
        if agent.positions:
            print(f"\nPositions Opened: {len(agent.positions)}")
            for i, pos in enumerate(agent.positions, 1):
                print(f"  {i}. {pos['side']} {pos['quantity']:.6f} {pos['symbol']} @ ${pos['price']:.2f}")
        
    except KeyboardInterrupt:
        print("\n\nStopped by user")
        print(f"Made {agent.trades_executed} trades")


if __name__ == "__main__":
    run_aggressive_demo()
