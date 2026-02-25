# -*- coding: utf-8 -*-
"""
Simple Web UI Launcher - Shows your agent's performance
"""
import sys
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

from flask import Flask, render_template, jsonify
from flask_cors import CORS
import json
from pathlib import Path
from real_wallet import RealWalletTrader

app = Flask(__name__)
CORS(app)

# Your wallet
WALLET_ADDRESS = "0x83cc3b8731f6344D7DA6529566D94ACf30271C08"

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/wallet')
def wallet_info():
    """Get real wallet balance"""
    try:
        wallet = RealWalletTrader(WALLET_ADDRESS)
        balances = wallet.get_all_balances()
        return jsonify({
            'address': WALLET_ADDRESS,
            'balances': balances,
            'connected': True
        })
    except Exception as e:
        return jsonify({'error': str(e), 'connected': False}), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print(" "*15 + "AI TRADING AGENT - WEB DASHBOARD")
    print("="*70)
    print("\n🌐 Starting web server...")
    print("\n📊 Open your browser to:")
    print("   http://localhost:5000")
    print("\n✨ Features:")
    print("   • Live wallet balance")
    print("   • Trading signals")
    print("   • Agent health (GMAC)")
    print("   • Performance charts")
    print("\n💡 Keep this window open while using the dashboard")
    print("   Press Ctrl+C to stop\n")
    
    app.run(debug=False, port=5000, use_reloader=False)
