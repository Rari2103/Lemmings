# -*- coding: utf-8 -*-
"""
Uniswap API Integration - No personal API key required!
Uses Uniswap's public APIs and on-chain data
"""
import requests
import json
import time
from typing import Dict, List, Optional
import logging
from config import ENABLE_PAPER_TRADING

logger = logging.getLogger(__name__)


class UniswapTrader:
    """Wrapper for Uniswap API and DEX trading"""
    
    def __init__(self):
        # Uniswap public API endpoints
        self.api_base = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
        self.info_api = "https://api.uniswap.org/v1"
        
        # Paper trading setup
        self.paper_trading = ENABLE_PAPER_TRADING
        self.paper_balance = {
            "USDT": 1000.0,
            "WETH": 0.0,
            "USDC": 0.0,
            "DAI": 0.0
        }
        self.paper_positions = []
        
        logger.info(f"Uniswap Trader initialized (Paper: {self.paper_trading})")
    
    def get_token_price(self, token_address: str) -> Optional[float]:
        """Get current token price from Uniswap"""
        try:
            # Query Uniswap v3 subgraph
            query = """
            {
              token(id: "%s") {
                derivedETH
                symbol
                name
              }
              bundle(id: "1") {
                ethPriceUSD
              }
            }
            """ % token_address.lower()
            
            response = requests.post(
                self.api_base,
                json={'query': query},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and data['data']['token']:
                    token = data['data']['token']
                    eth_price = float(data['data']['bundle']['ethPriceUSD'])
                    token_eth = float(token['derivedETH'])
                    token_usd = token_eth * eth_price
                    return token_usd
            
            return None
        except Exception as e:
            logger.error(f"Failed to get price for {token_address}: {e}")
            return None
    
    def get_ticker(self, symbol: str) -> Optional[Dict]:
        """Get ticker data for a trading pair"""
        # Common token addresses on Ethereum mainnet
        tokens = {
            "WETH_USDT": {
                "base": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
                "quote": "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # USDT
            },
            "WETH_USDC": {
                "base": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
                "quote": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC
            },
            "USDC_USDT": {
                "base": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC
                "quote": "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # USDT
            }
        }
        
        if symbol not in tokens:
            logger.warning(f"Unknown symbol: {symbol}")
            return None
        
        try:
            pair = tokens[symbol]
            base_price = self.get_token_price(pair["base"])
            
            if base_price:
                return {
                    "symbol": symbol,
                    "last": base_price,
                    "bid": base_price * 0.999,
                    "ask": base_price * 1.001,
                    "volume": 1000000,  # Simulated
                    "timestamp": int(time.time() * 1000)
                }
            
            return None
        except Exception as e:
            logger.error(f"Failed to get ticker for {symbol}: {e}")
            return None
    
    def get_candlesticks(self, symbol: str, timeframe: str = "1h", count: int = 100) -> List[Dict]:
        """Get historical candlestick data"""
        try:
            # For demo, generate realistic looking candles from current price
            ticker = self.get_ticker(symbol)
            if not ticker:
                return []
            
            current_price = ticker["last"]
            candles = []
            
            # Generate historical candles with some variance
            for i in range(count, 0, -1):
                variance = (hash(f"{symbol}{i}") % 100) / 1000 - 0.05  # -5% to +5%
                price = current_price * (1 + variance)
                
                candles.append({
                    "timestamp": int((time.time() - i * 3600) * 1000),
                    "open": price * 0.998,
                    "high": price * 1.002,
                    "low": price * 0.997,
                    "close": price,
                    "volume": 1000000 + (hash(f"{i}") % 500000)
                })
            
            return candles
        except Exception as e:
            logger.error(f"Failed to get candlesticks: {e}")
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
            
            order_id = f"UNI_PAPER_{int(time.time() * 1000)}"
            logger.info(f"Paper trade: {side} {quantity:.6f} {symbol} @ ${exec_price:.2f}")
            
            return {
                "success": True,
                "order_id": order_id,
                "symbol": symbol,
                "side": side,
                "quantity": quantity,
                "price": exec_price,
                "paper_trade": True,
                "dex": "Uniswap"
            }
        except Exception as e:
            logger.error(f"Paper trade failed: {e}")
            return {"success": False, "error": str(e)}
    
    def get_market_data(self, symbols: List[str]) -> Dict:
        """Get comprehensive market data for multiple symbols"""
        market_data = {}
        
        for symbol in symbols:
            ticker = self.get_ticker(symbol)
            candles = self.get_candlesticks(symbol, "1h", 50)
            
            if ticker and candles:
                market_data[symbol] = {
                    "ticker": ticker,
                    "candles": candles
                }
        
        return market_data
