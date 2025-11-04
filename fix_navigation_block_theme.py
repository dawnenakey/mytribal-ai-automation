#!/usr/bin/env python3
"""
Help troubleshoot navigation menu for block themes.
Provides specific guidance based on theme type.
"""

import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL = "https://mytribal.ai"

def detect_theme():
    """Try to detect the WordPress theme."""
    try:
        response = requests.get(WP_URL, verify=False, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check for theme indicators
            body_class = soup.find('body')
            if body_class:
                classes = body_class.get('class', [])
                theme_indicators = [c for c in classes if 'theme' in c.lower() or 'twenty' in c.lower()]
                if theme_indicators:
                    return theme_indicators[0]
            
            # Check for block theme indicators
            if soup.find(class_=lambda x: x and 'wp-block' in str(x)):
                return "Block Theme (likely Twenty Twenty-Three/Four)"
            
            return "Unknown (likely block theme)"
    except:
        return "Could not detect"

def print_solution():
    theme = detect_theme()
    print("="*70)
    print("NAVIGATION MENU FIX FOR BLOCK THEMES")
    print("="*70)
    print(f"\n🔍 Detected: {theme}")
    
    print("\n" + "="*70)
    print("SOLUTION: Add Navigation via Site Editor")
    print("="*70)
    
    print("\n📋 STEP-BY-STEP INSTRUCTIONS:")
    print("\n1. CREATE THE MENU (if not done yet):")
    print("   → Go to: https://mytribal.ai/wp-admin/nav-menus.php")
    print("   → Create new menu: 'Main Menu'")
    print("   → Add pages: Services, Case Studies, About Us, Contact")
    print("   → Click 'Save Menu'")
    
    print("\n2. ADD NAVIGATION TO HEADER:")
    print("   → Go to: https://mytribal.ai/wp-admin/site-editor.php")
    print("   → Click 'Templates' in left sidebar")
    print("   → Click 'Header' template")
    print("   → Click 'Edit' button")
    
    print("\n3. INSERT NAVIGATION BLOCK:")
    print("   → Click '+' button (top left or in editor)")
    print("   → Type 'Navigation' in search box")
    print("   → Click on 'Navigation' block")
    
    print("\n4. SELECT YOUR MENU:")
    print("   → In right sidebar, find 'Menu' dropdown")
    print("   → Select 'Main Menu' (the one you created)")
    
    print("\n5. SAVE:")
    print("   → Click 'Save' button (top right)")
    print("   → Menu should now appear on your site!")
    
    print("\n" + "="*70)
    print("ALTERNATIVE: Via Customizer")
    print("="*70)
    print("\nSome themes support Customizer:")
    print("   → Go to: https://mytribal.ai/wp-admin/customize.php")
    print("   → Look for 'Navigation' or 'Menus' section")
    print("   → Select your menu and assign location")
    
    print("\n" + "="*70)
    print("QUICK LINKS")
    print("="*70)
    print(f"\n🔗 Site Editor: {WP_URL}/wp-admin/site-editor.php")
    print(f"🔗 Menus: {WP_URL}/wp-admin/nav-menus.php")
    print(f"🔗 Customizer: {WP_URL}/wp-admin/customize.php")
    
    print("\n" + "="*70)
    print("TROUBLESHOOTING")
    print("="*70)
    print("\n❓ Can't find Site Editor?")
    print("   → Make sure you're logged in as Administrator")
    print("   → Some hosts disable Site Editor - use Customizer instead")
    
    print("\n❓ Navigation block doesn't show menu?")
    print("   → Make sure menu exists: Appearance → Menus")
    print("   → Make sure menu has pages added")
    print("   → Try refreshing the page after saving")
    
    print("\n❓ Menu still not showing?")
    print("   → Check if theme has menu location settings")
    print("   → Try Appearance → Customize → Menus")
    print("   → Clear browser cache (Cmd+Shift+R or Ctrl+Shift+R)")
    
    print("\n✅ After adding, visit your site to verify!")
    print("="*70 + "\n")

if __name__ == "__main__":
    print_solution()


