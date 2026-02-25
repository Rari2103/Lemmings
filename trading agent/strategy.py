# -*- coding: utf-8 -*-
"""
Trading strategies and decision logic
"""
import numpy as np
from typing import Dict, List
import logging
from config import (
    RSI_PERIOD, RSI_OVERSOLD, RSI_OVERBOUGHT,
    MA_FAST, MA_SLOW
)

logger = logging.getLogger(__name__)


class TradingStrategy:
    """Base class for trading strategies"""
    
    def __init__(self):
        self.name = "base_strategy"
    
    def calculate_rsi(self, prices: List[float], period: int = RSI_PERIOD) -> float:
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return 50.0
        
        deltas = np.diff(prices)
        gains = deltas.copy()
        losses = deltas.copy()
        gains[gains < 0] = 0
        losses[losses > 0] = 0
        losses = abs(losses)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_sma(self, prices: List[float], period: int) -> float:
        """Calculate Simple Moving Average"""
        if len(prices) < period:
            return prices[-1] if prices else 0
        return np.mean(prices[-period:])
    
    def calculate_momentum(self, prices: List[float], period: int = 10) -> float:
        """Calculate price momentum"""
        if len(prices) < period:
            return 0.0
        return (prices[-1] - prices[-period]) / prices[-period]


class MomentumStrategy(TradingStrategy):
    """Momentum-based trading strategy"""
    
    def __init__(self):
        super().__init__()
        self.name = "momentum_strategy"
    
    def analyze(self, market_data: Dict) -> Dict:
        """Analyze market using momentum indicators"""
        signals = []
        
        for symbol, data in market_data.items():
            if not data.get("candles") or len(data["candles"]) < MA_SLOW:
                continue
            
            prices = [c["close"] for c in data["candles"]]
            current_price = prices[-1]
            
            # Calculate indicators
            rsi = self.calculate_rsi(prices)
            ma_fast = self.calculate_sma(prices, MA_FAST)
            ma_slow = self.calculate_sma(prices, MA_SLOW)
            momentum = self.calculate_momentum(prices, 10)
            
            # Generate signal
            signal_strength = 0
            reasons = []
            
            # RSI signals
            if rsi < RSI_OVERSOLD:
                signal_strength += 2
                reasons.append(f"RSI oversold ({rsi:.1f})")
            elif rsi > RSI_OVERBOUGHT:
                signal_strength -= 2
                reasons.append(f"RSI overbought ({rsi:.1f})")
            
            # Moving average crossover
            if ma_fast > ma_slow * 1.01:
                signal_strength += 2
                reasons.append("MA bullish crossover")
            elif ma_fast < ma_slow * 0.99:
                signal_strength -= 2
                reasons.append("MA bearish crossover")
            
            # Momentum
            if momentum > 0.02:
                signal_strength += 1
                reasons.append(f"Strong momentum ({momentum:.2%})")
            elif momentum < -0.02:
                signal_strength -= 1
                reasons.append(f"Weak momentum ({momentum:.2%})")
            
            # Determine action
            action = "HOLD"
            confidence = abs(signal_strength) / 8.0
            
            if signal_strength >= 3:
                action = "BUY"
            elif signal_strength <= -3:
                action = "SELL"
            
            signals.append({
                "symbol": symbol,
                "action": action,
                "confidence": min(confidence, 1.0),
                "price": current_price,
                "rsi": rsi,
                "momentum": momentum,
                "reasons": reasons,
                "signal_strength": signal_strength
            })
        
        if signals:
            signals.sort(key=lambda x: abs(x["signal_strength"]), reverse=True)
            return signals[0]
        
        return {"action": "HOLD", "confidence": 0.0, "reasons": ["No data"]}


def get_strategy(strategy_type: str) -> TradingStrategy:
    """Factory function to get strategy instance"""
    if strategy_type == "momentum":
        return MomentumStrategy()
    return MomentumStrategy()
