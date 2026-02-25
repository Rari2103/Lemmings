# -*- coding: utf-8 -*-
"""
Enhanced Real Wallet with Multiple RPC Endpoints
"""
from web3 import Web3
import logging
from typing import Dict, Optional
import time

logger = logging.getLogger(__name__)


class EnhancedWalletTrader:
    """Wallet connection with multiple RPC fallbacks"""
    
    def __init__(self, wallet_address: str):
        self.wallet_address = Web3.to_checksum_address(wallet_address)
        
        # Get API key from environment
        import os
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("ETH_RPC_API_KEY")
        
        # Multiple RPC endpoints with API key support
        if api_key:
            self.rpc_endpoints = [
                f"https://mainnet.infura.io/v3/{api_key}",
                f"https://eth-mainnet.g.alchemy.com/v2/{api_key}",
                "https://ethereum.publicnode.com",
                "https://rpc.ankr.com/eth"
            ]
        else:
            self.rpc_endpoints = [
                "https://ethereum.publicnode.com",
                "https://rpc.ankr.com/eth",
                "https://eth.llamarpc.com",
                "https://cloudflare-eth.com"
            ]
        
        self.w3 = None
        self._connect()
        
        # Cache for balance (reduces API calls)
        self._balance_cache = {}
        self._cache_time = 0
        self._cache_duration = 30  # seconds
    
    def _connect(self):
        """Try connecting to RPC endpoints"""
        for rpc_url in self.rpc_endpoints:
            try:
                w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={'timeout': 10}))
                if w3.is_connected():
                    self.w3 = w3
                    logger.info(f"Connected to {rpc_url}")
                    return
            except Exception as e:
                logger.debug(f"Failed to connect to {rpc_url}: {e}")
                continue
        
        raise Exception("Failed to connect to any RPC endpoint")
    
    # Token addresses
    tokens = {
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    }
    
    erc20_abi = [
        {"constant": True, "inputs": [{"name": "_owner", "type": "address"}],
         "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"},
        {"constant": True, "inputs": [], "name": "decimals",
         "outputs": [{"name": "", "type": "uint8"}], "type": "function"}
    ]
    
    def get_all_balances(self) -> Dict[str, float]:
        """Get all balances with caching"""
        # Check cache
        if time.time() - self._cache_time < self._cache_duration:
            if self._balance_cache:
                return self._balance_cache.copy()
        
        balances = {}
        
        try:
            # ETH balance
            eth_balance = self.w3.eth.get_balance(self.wallet_address)
            if eth_balance > 0:
                balances["ETH"] = float(self.w3.from_wei(eth_balance, 'ether'))
            
            # USDC balance (most important)
            usdc_address = self.tokens["USDC"]
            contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(usdc_address),
                abi=self.erc20_abi
            )
            balance = contract.functions.balanceOf(self.wallet_address).call()
            decimals = contract.functions.decimals().call()
            usdc_amount = balance / (10 ** decimals)
            if usdc_amount > 0:
                balances["USDC"] = float(usdc_amount)
            
            # Cache the result
            self._balance_cache = balances
            self._cache_time = time.time()
            
        except Exception as e:
            logger.error(f"Failed to get balances: {e}")
            # Return cached data if available
            if self._balance_cache:
                return self._balance_cache.copy()
        
        return balances
