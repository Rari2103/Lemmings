# -*- coding: utf-8 -*-
"""
Core AI Trading Agent with metabolism and survival mechanics
"""
import time
import json
import logging
from datetime import datetime
from typing import Dict, Optional
from trading import CryptoComTrader
from strategy import get_strategy
from config import *

logger = logging.getLogger(__name__)


class TradingAgent:
    """AI Trading Agent with life mechanics"""
    
    def __init__(self, name: str = "Agent"):
        self.name = name
        self.gmac = INITIAL_GMAC
        self.goodwill = INITIAL_GOODWILL
        self.alive = True
        self.survival_mode = False
        self.critical_mode = False
        
        # Trading components
        self.trader = CryptoComTrader()
        self.strategy = get_strategy(STRATEGY_TYPE)
        
        # Statistics
        self.heartbeats = 0
        self.trades_executed = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_pnl = 0.0
        self.daily_pnl = 0.0
        self.daily_trades = 0
        self.positions = []
        
        logger.info(f"Agent {self.name} initialized with {self.gmac} GMAC")
    
    def heartbeat(self) -> bool:
        """Process one heartbeat cycle"""
        if not self.alive:
            return False
        
        self.heartbeats += 1
        self.gmac -= GMAC_HEARTBEAT_COST
        
        logger.info(f"\n{'='*80}")
        logger.info(f"HEARTBEAT #{self.heartbeats} - Agent: {self.name}")
        logger.info(f"GMAC: {self.gmac:.2f} | Goodwill: {self.goodwill}")
        logger.info(f"Trades: {self.trades_executed} (W:{self.winning_trades} L:{self.losing_trades})")
        logger.info(f"P&L: ${self.total_pnl:.2f} (Today: ${self.daily_pnl:.2f})")
        
        # Check survival status
        self._check_survival_status()
        
        if not self.alive:
            return False
        
        # Get market data
        market_data = self._fetch_market_data()
        
        # Analyze and trade
        if not self.critical_mode:
            signal = self._analyze_market(market_data)
            self._execute_trade_decision(signal)
        else:
            logger.warning("Critical mode - skipping trading to conserve GMAC")
        
        logger.info("="*80)
        return True
    
    def _check_survival_status(self):
        """Check and update survival status"""
        if self.gmac <= GMAC_DEATH_THRESHOLD:
            self.alive = False
            logger.error(f"Agent {self.name} has died - GMAC depleted")
            return
        
        if self.gmac <= GMAC_CRITICAL_THRESHOLD:
            if not self.critical_mode:
                self.critical_mode = True
                logger.error(f"CRITICAL MODE - GMAC: {self.gmac:.2f}")
        elif self.gmac <= GMAC_SURVIVAL_THRESHOLD:
            if not self.survival_mode:
                self.survival_mode = True
                logger.warning(f"SURVIVAL MODE - GMAC: {self.gmac:.2f}")
        else:
            self.survival_mode = False
            self.critical_mode = False
    
    def _fetch_market_data(self) -> Dict:
        """Fetch market data and consume GMAC"""
        self.gmac -= GMAC_API_CALL_COST * len(TRADING_PAIRS)
        logger.debug(f"Fetching market data... (GMAC: {self.gmac:.2f})")
        return self.trader.get_market_data(TRADING_PAIRS)
    
    def _analyze_market(self, market_data: Dict) -> Dict:
        """Analyze market and generate signal"""
        self.gmac -= GMAC_INFERENCE_BASE_COST
        signal = self.strategy.analyze(market_data)
        
        if signal.get("action") != "HOLD":
            logger.info(f"Signal: {signal['action']} {signal.get('symbol')} "
                       f"(confidence: {signal['confidence']:.1%})")
            if signal.get("reasons"):
                logger.info(f"   Reasons: {', '.join(signal['reasons'])}")
        
        return signal
    
    def _execute_trade_decision(self, signal: Dict):
        """Decide whether to execute trade"""
        if signal.get("action") == "HOLD":
            logger.info("No trade signal")
            return
        
        confidence_threshold = 0.70
        if self.survival_mode:
            confidence_threshold = 0.85
        
        if signal.get("confidence", 0) < confidence_threshold:
            logger.info(f"Signal confidence {signal['confidence']:.1%} "
                       f"below threshold {confidence_threshold:.1%}")
            return
        
        # Execute trade
        self._execute_trade(signal)
    
    def _execute_trade(self, signal: Dict):
        """Execute a trade"""
        self.gmac -= GMAC_TRADE_COST
        
        symbol = signal["symbol"]
        side = signal["action"]
        price = signal["price"]
        
        # Calculate position size
        balance = self.trader.get_balance()
        quote_currency = symbol.split("_")[1]
        available = balance.get(quote_currency, 0)
        
        position_size_pct = MAX_POSITION_SIZE
        if self.survival_mode:
            position_size_pct = SURVIVAL_MODE_POSITION_SIZE
        
        trade_amount = available * position_size_pct
        quantity = trade_amount / price
        
        # Execute order
        result = self.trader.place_order(symbol, side, "MARKET", quantity, price)
        
        if result.get("success"):
            self.trades_executed += 1
            self.daily_trades += 1
            logger.info(f"TRADE EXECUTED: {side} {quantity:.6f} {symbol} @ ${price:.2f}")
            
            # Track position
            self.positions.append({
                "symbol": symbol,
                "side": side,
                "entry_price": price,
                "quantity": quantity,
                "timestamp": time.time()
            })
            
            # Earn goodwill
            self.goodwill += GOODWILL_TASK_COMPLETE
            logger.info(f"Goodwill: {self.goodwill} (+{GOODWILL_TASK_COMPLETE})")
        else:
            logger.error(f"Trade failed: {result.get('error')}")


def run_agent_demo(cycles: int = 5):
    """Run agent for a few cycles to demonstrate"""
    print("\n" + "="*80)
    print("STARTING AI TRADING AGENT DEMO")
    print("="*80)
    
    agent = TradingAgent("Demo-Agent")
    
    for i in range(cycles):
        print(f"\n[Cycle {i+1}/{cycles}]")
        if not agent.heartbeat():
            print("Agent stopped")
            break
        time.sleep(2)  # Wait 2 seconds between cycles
    
    print("\n" + "="*80)
    print("DEMO COMPLETE")
    print("="*80)
    print(f"\nFinal Status:")
    print(f"  Agent: {agent.name}")
    print(f"  GMAC: {agent.gmac:.2f}")
    print(f"  Goodwill: {agent.goodwill}")
    print(f"  Heartbeats: {agent.heartbeats}")
    print(f"  Trades: {agent.trades_executed}")
    print(f"  Balance: {agent.trader.get_balance()}")
    print()
