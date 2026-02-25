"""
Quick test to verify the trading agent setup
"""
print("🔍 Testing Trading Agent Setup...\n")

# Test 1: Python version
print("1. Python Version")
import sys
print(f"   ✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\n")

# Test 2: Dependencies
print("2. Dependencies")
try:
    import numpy
    print(f"   ✅ numpy")
    import requests
    print(f"   ✅ requests")
    import flask
    print(f"   ✅ flask")
    print()
except ImportError as e:
    print(f"   ❌ {e}\n")
    sys.exit(1)

# Test 3: Configuration
print("3. Configuration")
try:
    import config
    print(f"   ✅ Config loaded")
    print(f"      Paper Trading: {config.ENABLE_PAPER_TRADING}")
    print(f"      Strategy: {config.STRATEGY_TYPE}")
    print(f"      Initial GMAC: {config.INITIAL_GMAC}")
    print()
except Exception as e:
    print(f"   ❌ {e}\n")
    sys.exit(1)

print("="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
print("\n🚀 Your trading agent is ready!")
print("\nTo start:")
print("   python simple_demo.py")
print()
