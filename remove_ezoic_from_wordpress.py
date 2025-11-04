#!/usr/bin/env python3
"""
Check and provide instructions for removing Ezoic from WordPress.
Uses WordPress REST API to check for Ezoic plugins and provide removal instructions.
"""

import os
import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

WP_URL = os.getenv("WP_URL", "https://mytribal.ai").rstrip('/')
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

def create_auth_header():
    """Create authentication header for WordPress REST API"""
    if not WP_USERNAME or not WP_APP_PASSWORD:
        return None
    credentials = f"{WP_USERNAME}:{WP_APP_PASSWORD}"
    token = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {token}"}

def get_active_plugins():
    """Get list of active plugins via REST API"""
    auth_header = create_auth_header()
    if not auth_header:
        print("❌ WordPress credentials not found in .env file")
        return None
    
    try:
        url = f"{WP_URL}/wp-json/wp/v2/plugins"
        response = requests.get(url, headers=auth_header, verify=False, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("❌ Authentication failed. Check your WP_USERNAME and WP_APP_PASSWORD in .env")
            return None
        elif response.status_code == 404:
            print("⚠️ Plugins endpoint not available via REST API")
            print("   WordPress REST API may not support plugin management")
            return None
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error checking plugins: {e}")
        return None

def check_ezoic_plugins():
    """Check for Ezoic plugins and provide removal instructions"""
    print("="*70)
    print("EZOIC PLUGIN CHECKER")
    print("="*70)
    
    print(f"\n🔍 Checking WordPress site: {WP_URL}")
    
    plugins = get_active_plugins()
    
    if plugins is None:
        print("\n" + "="*70)
        print("MANUAL REMOVAL INSTRUCTIONS")
        print("="*70)
        print_manual_instructions()
        return
    
    ezoic_plugins = []
    if isinstance(plugins, list):
        for plugin in plugins:
            plugin_name = plugin.get('name', '')
            plugin_status = plugin.get('status', '')
            if 'ezoic' in plugin_name.lower():
                ezoic_plugins.append({
                    'name': plugin_name,
                    'status': plugin_status,
                    'file': plugin.get('plugin', '')
                })
    
    print("\n" + "="*70)
    if ezoic_plugins:
        print(f"⚠️ Found {len(ezoic_plugins)} Ezoic plugin(s):")
        print("="*70)
        for plugin in ezoic_plugins:
            status_icon = "🟢 ACTIVE" if plugin['status'] == 'active' else "⚪ INACTIVE"
            print(f"\n   {status_icon}: {plugin['name']}")
            print(f"   File: {plugin['file']}")
    else:
        print("✅ No Ezoic plugins found (or they're not accessible via API)")
        print("="*70)
        print("\n💡 This might mean:")
        print("   - Ezoic is using Cloudflare integration (no WordPress plugin)")
        print("   - Ezoic plugins are named differently")
        print("   - Plugins are already removed")
    
    print("\n" + "="*70)
    print("REMOVAL INSTRUCTIONS")
    print("="*70)
    print_manual_instructions()
    
    if ezoic_plugins:
        print("\n" + "="*70)
        print("AUTOMATIC DEACTIVATION (if API supports it)")
        print("="*70)
        print("\n⚠️ WordPress REST API typically doesn't allow plugin management")
        print("   for security reasons. You'll need to deactivate manually.")
        print("\n   However, you can try:")
        print("   1. Log into WordPress: https://mytribal.ai/wp-admin")
        print("   2. Go to: Plugins → Installed Plugins")
        print("   3. Find each Ezoic plugin listed above")
        print("   4. Click 'Deactivate' for each one")
        print("   5. Optionally click 'Delete' to remove completely")

def print_manual_instructions():
    """Print manual removal instructions"""
    print("\n📋 STEP-BY-STEP REMOVAL GUIDE:")
    print("\n1. LOG INTO WORDPRESS ADMIN:")
    print("   → Visit: https://mytribal.ai/wp-admin")
    print("   → Enter your admin credentials")
    
    print("\n2. GO TO PLUGINS PAGE:")
    print("   → Click 'Plugins' in left sidebar")
    print("   → Click 'Installed Plugins'")
    
    print("\n3. FIND EZOIC PLUGINS:")
    print("   → Look for plugins with 'Ezoic' in the name")
    print("   → Common Ezoic plugins include:")
    print("      - Ezoic")
    print("      - Ezoic Speed")
    print("      - Ezoic Ad Tester")
    print("      - Ezoic Integration")
    print("      - Ezoic Cloudflare Integration")
    
    print("\n4. DEACTIVATE EZOIC PLUGINS:")
    print("   → For each Ezoic plugin, click 'Deactivate'")
    print("   → OR select multiple → Bulk Actions → Deactivate → Apply")
    
    print("\n5. (OPTIONAL) DELETE EZOIC PLUGINS:")
    print("   → After deactivating, you can click 'Delete'")
    print("   → This completely removes the plugin files")
    print("   → ⚠️ You can reinstall later if needed")
    
    print("\n6. CHECK FOR EZOIC IN CODE:")
    print("   → Go to: Settings → Insert Headers and Footers")
    print("   → Check for any Ezoic scripts in header/footer")
    print("   → Remove any Ezoic code if found")
    
    print("\n7. CLEAR CACHE:")
    print("   → If you use caching plugins (WP Rocket, W3 Total Cache, etc.)")
    print("   → Clear all cache")
    print("   → Clear browser cache too")
    
    print("\n8. VERIFY REMOVAL:")
    print("   → Visit your homepage: https://mytribal.ai")
    print("   → Check that Ezoic ads are no longer showing")
    print("   → Check page source (Ctrl+U) for Ezoic scripts")
    print("   → Look for 'ezoic' in the HTML source")
    
    print("\n" + "="*70)
    print("IMPORTANT NOTES")
    print("="*70)
    print("\n⚠️ If Ezoic is using Cloudflare integration:")
    print("   - There may be no WordPress plugin")
    print("   - You need to remove Ezoic from Cloudflare dashboard")
    print("   - Go to Cloudflare → Apps → Remove Ezoic")
    
    print("\n⚠️ If ads still showing after plugin removal:")
    print("   - Check theme files for hardcoded Ezoic code")
    print("   - Check widget areas for Ezoic widgets")
    print("   - Clear all caches (WordPress, browser, CDN)")
    print("   - Wait 24-48 hours for DNS changes to propagate")
    
    print("\n✅ After Ezoic is removed:")
    print("   - You can proceed with Media.net setup")
    print("   - See MEDIANET_SETUP_GUIDE.md for next steps")

if __name__ == "__main__":
    import base64
    check_ezoic_plugins()

