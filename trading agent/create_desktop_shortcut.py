# -*- coding: utf-8 -*-
"""
Create Desktop Shortcut - Makes it easy to launch
"""
import os
import sys
from pathlib import Path

# Get paths
desktop = Path.home() / "Desktop"
trading_agent_dir = Path(__file__).parent.absolute()
bat_file = trading_agent_dir / "START_DASHBOARD.bat"

print("="*70)
print(" "*15 + "CREATING DESKTOP SHORTCUT")
print("="*70)
print(f"\nTrading Agent Directory: {trading_agent_dir}")
print(f"Desktop: {desktop}")
print(f"Launcher: {bat_file}")

# Create shortcut using PowerShell
shortcut_path = desktop / "AI Trading Agent.lnk"

ps_script = f"""
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
$Shortcut.TargetPath = '{bat_file}'
$Shortcut.WorkingDirectory = '{trading_agent_dir}'
$Shortcut.Description = 'AI Trading Agent Dashboard'
$Shortcut.Save()
"""

try:
    os.system(f'powershell -Command "{ps_script}"')
    print(f"\n✅ Desktop shortcut created!")
    print(f"   Location: {shortcut_path}")
    print(f"\n🚀 Double-click 'AI Trading Agent' on your desktop to launch!")
except Exception as e:
    print(f"\n❌ Failed to create shortcut: {e}")
    print(f"\n💡 You can manually double-click:")
    print(f"   {bat_file}")
