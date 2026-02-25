# -*- coding: utf-8 -*-
"""
Real Wallet Integration - Connect to your Ethereum wallet
"""
from web3 import Web3
from eth_account import Account
import json
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class RealWalletTrader:
    """Connect to a real Ethereum wallet and Uniswap"""
    
    def __init__(self, wallet_address: str, private_key: Optional[str] = None, rpc_url: str = None):
        """
        Initialize wallet connection
        
        Args:
            wallet_address: Your Ethereum wallet address
            private_key: Private key for signing transactions (optional for read-only)
            rpc_url: Ethereum RPC endpoint (defaults to Infura)
        """
        self.wallet_address = Web3.to_checksum_address(wallet_address)
        self.private_key = private_key
        
        # Connect to Ethereum (using public RPC)
        if rpc_url:
            self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        else:
            # Use public Ethereum mainnet RPC
            self.w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
        
        # Check connection
        if not self.w3.is_connected():
            raise Exception("Failed to connect to Ethereum network")
        
        logger.info(f"Connected to Ethereum (Chain ID: {self.w3.eth.chain_id})")
        logger.info(f"Wallet: {self.wallet_address}")
        
        # ERC20 Token addresses on Ethereum Mainnet
        self.tokens = {
            "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F"
        }
        
        # ERC20 ABI (minimal - for balance checking)
        self.erc20_abi = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "symbol",
                "outputs": [{"name": "", "type": "string"}],
                "type": "function"
            }
        ]
    
    def get_eth_balance(self) -> float:
        """Get ETH balance"""
        try:
            balance_wei = self.w3.eth.get_balance(self.wallet_address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            return float(balance_eth)
        except Exception as e:
            logger.error(f"Failed to get ETH balance: {e}")
            return 0.0
    
    def get_token_balance(self, token_symbol: str) -> float:
        """Get ERC20 token balance"""
        try:
            if token_symbol not in self.tokens:
                logger.warning(f"Unknown token: {token_symbol}")
                return 0.0
            
            token_address = self.tokens[token_symbol]
            contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=self.erc20_abi
            )
            
            # Get balance
            balance = contract.functions.balanceOf(self.wallet_address).call()
            decimals = contract.functions.decimals().call()
            
            # Convert to human-readable
            balance_float = balance / (10 ** decimals)
            return float(balance_float)
        
        except Exception as e:
            logger.error(f"Failed to get {token_symbol} balance: {e}")
            return 0.0
    
    def get_all_balances(self) -> Dict[str, float]:
        """Get all token balances"""
        balances = {}
        
        # ETH balance
        eth_balance = self.get_eth_balance()
        if eth_balance > 0:
            balances["ETH"] = eth_balance
        
        # Token balances
        for token_symbol in self.tokens.keys():
            balance = self.get_token_balance(token_symbol)
            if balance > 0:
                balances[token_symbol] = balance
        
        return balances
