# -*- coding: utf-8 -*-
"""
Crypto.com API wrapper and trading execution
"""
import hashlib
import hmac
import time
import requests
import json
from typing import Dict, List, Optional
import logging
from config import (
    CRYPTO_COM_API_KEY,
    CRYPTO_COM_SECRET_KEY,
    API_BASE_URL,
    ENABLE_PAPER_TRADING
)

logger = logging.getLogger(__name__)


class CryptoComTrader:
    """Wrapper for Crypto.com Exchange API"""
    
    def __init__(self):
        self.api_key = CRYPTO_COM_API_KEY
        self.secret_key = CRYPTO_COM_SECRET_KEY
        self.base_url = API_BASE_URL
        self.paper_trading = ENABLE_PAPER_TRADING
        self.paper_balance = {"USDT": 1000.0, "BTC": 0.0, "ETH": 0.0, "CRO": 0.0}
        self.paper_positions = []
    
    def get_ticker(self, symbol: str) -> Optional[Dict]:
        """Get current ticker price"""
        try:
            url = f"{self.base_url}public/get-ticker"
            params = {"instrument_name": symbol}
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get("code") == 0 and data.get("result"):
                result = data["result"]["data"][0]
                return {
                    "symbol": symbol,
                    "last": float(result.get("a", 0)),
                    "bid": float(result.get("b", 0)),
                    "ask": float(result.get("a", 0)),
                    "volume": float(result.get("v", 0)),
                    "timestamp": result.get("t", 0)
                }
            return None
        except Exception as e:
            logger.error(f"Failed to get ticker for {symbol}: {e}")
            return None
    
    def get_candlesticks(self, symbol: str, timeframe: str = "1m", count: int = 100) -> List[Dict]:
        """Get historical candlestick data"""
        try:
            url = f"{self.base_url}public/get-candlestick"
            params = {"instrument_name": symbol, "timeframe": timeframe}
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get("code") == 0 and data.get("result"):
                candles = data["result"]["data"][-count:]
                return [{
                    "timestamp": c["t"],
                    "open": float(c["o"]),
                    "high": float(c["h"]),
                    "low": float(c["l"]),
                    "close": float(c["c"]),
                    "volume": float(c["v"])
                } for c in candles]
            return []
        except Exception as e:
            logger.error(f"Failed to get candlesticks for {symbol}: {e}")
            return []
    
    def get_balance(self) -> Dict[str, float]:
        """Get account balance"""
        if self.paper_trading:
            return self.paper_balance.copy()
        return {}
    
    def place_order(self, symbol: str, side: str, order_type: str, 
                   quantity: float, price: float = None) -> Dict:
        """Place an order (paper trading simulation)"""
        if self.paper_trading:
            return self._place_paper_order(symbol, side, order_type, quantity, price)
        return {"success": False, "error": "Live trading not implemented"}
    
    def _place_paper_order(self, symbol: str, side: str, order_type: str,
                          quantity: float, price: float = None) -> Dict:
        """Simulate order execution for paper trading"""
        ticker = self.get_ticker(symbol)
        if not ticker:
            return {"success": False, "error": "Failed to get ticker price"}
        
        exec_price = price if price and order_type == "LIMIT" else ticker["last"]
        base_currency = symbol.split("_")[0]
        quote_currency = symbol.split("_")[1]
        
        try:
            if side == "BUY":
                cost = quantity * exec_price
                if self.paper_balance.get(quote_currency, 0) < cost:
                    return {"success": False, "error": "Insufficient balance"}
                
                self.paper_balance[quote_currency] -= cost
                self.paper_balance[base_currency] = self.paper_balance.get(base_currency, 0) + quantity
            
            elif side == "SELL":
                if self.paper_balance.get(base_currency, 0) < quantity:
                    return {"success": False, "error": "Insufficient balance"}
                
                self.paper_balance[base_currency] -= quantity
                revenue = quantity * exec_price
                self.paper_balance[quote_currency] = self.paper_balance.get(quote_currency, 0) + revenue
            
            order_id = f"PAPER_{int(time.time() * 1000)}"
            logger.info(f"Paper trade: {side} {quantity:.6f} {symbol} @ ${exec_price:.2f}")
            
            return {
                "success": True,
                "order_id": order_id,
                "symbol": symbol,
                "side": side,
                "quantity": quantity,
                "price": exec_price,
                "paper_trade": True
            }
        except Exception as e:
            logger.error(f"Paper trade failed: {e}")
            return {"success": False, "error": str(e)}
    
    def get_market_data(self, symbols: List[str]) -> Dict:
        """Get comprehensive market data for multiple symbols"""
        market_data = {}
        
        for symbol in symbols:
            ticker = self.get_ticker(symbol)
            candles = self.get_candlesticks(symbol, "5m", 50)
            
            if ticker and candles:
                market_data[symbol] = {
                    "ticker": ticker,
                    "candles": candles
                }
        
        return market_data
