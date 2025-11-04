#!/usr/bin/env python3
"""
Add Privacy Policy, About Us, and Contact pages to WordPress navigation menu.
Uses WordPress REST API to update menu items.
"""

import os
import json
import base64
import ssl
import requests
from dotenv import load_dotenv
import urllib3

# Load environment variables from .env if available
load_dotenv()

WP_URL = os.getenv("WP_URL", "https://mytribal.ai").rstrip('/')
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def create_auth_header():
    if not WP_USERNAME or not WP_APP_PASSWORD:
        return None
    credentials = f"{WP_USERNAME}:{WP_APP_PASSWORD}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


def get_pages():
    """Get all published pages."""
    try:
        headers = {
            'Authorization': create_auth_header(),
            'Content-Type': 'application/json',
        }
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Get pages with slugs we need
        pages_to_find = ['privacy-policy', 'about', 'contact']
        pages_map = {}
        
        for slug in pages_to_find:
            url = f"{WP_URL}/wp-json/wp/v2/pages?slug={slug}"
            resp = requests.get(url, headers=headers, verify=False, timeout=30)
            if resp.status_code == 200:
                pages = resp.json()
                if pages:
                    pages_map[slug] = pages[0]
                    print(f"✅ Found page: {slug} (ID: {pages[0]['id']})")
                else:
                    print(f"⚠️ Page not found: {slug}")
            else:
                print(f"⚠️ Error fetching page {slug}: {resp.status_code}")
        
        return pages_map
    except Exception as e:
        print(f"❌ Error getting pages: {e}")
        return {}


def get_menus():
    """Get all navigation menus."""
    try:
        headers = {
            'Authorization': create_auth_header(),
            'Content-Type': 'application/json',
        }
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Try standard WordPress REST API menus endpoint (if available)
        url = f"{WP_URL}/wp-json/wp/v2/menus"
        resp = requests.get(url, headers=headers, verify=False, timeout=30)
        
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 404:
            # Try wp-api-menus plugin endpoint
            url = f"{WP_URL}/wp-json/wp-api-menus/v2/menus"
            resp = requests.get(url, headers=headers, verify=False, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            else:
                print("⚠️ Menu endpoints not available via REST API")
                return None
        else:
            print(f"⚠️ Unexpected response: {resp.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Error getting menus: {e}")
        return None


def add_pages_to_menu_rest_api(pages_map):
    """
    Attempt to add pages to menu via REST API.
    Note: This requires wp-api-menus plugin or custom endpoint.
    """
    print("\n📝 Attempting to add pages to menu via REST API...")
    
    menus = get_menus()
    if not menus:
        print("❌ Menu API endpoints not available. See manual instructions below.")
        return False
    
    print(f"✅ Found {len(menus)} menu(s)")
    
    # Try to find primary/main menu
    primary_menu = None
    for menu in menus:
        if menu.get('name', '').lower() in ['primary', 'main', 'header', 'navigation']:
            primary_menu = menu
            break
    
    if not primary_menu and menus:
        primary_menu = menus[0]  # Use first menu if no primary found
    
    if not primary_menu:
        print("❌ No menu found")
        return False
    
    print(f"📋 Using menu: {primary_menu.get('name')} (ID: {primary_menu.get('id')})")
    
    # This would require wp-api-menus plugin or custom endpoint
    # For now, provide manual instructions
    return False


def print_manual_instructions(pages_map):
    """Print manual instructions for adding pages to menu."""
    print("\n" + "="*70)
    print("MANUAL INSTRUCTIONS: Add Pages to Navigation Menu")
    print("="*70)
    print("\nWordPress REST API doesn't natively support menu management.")
    print("Please add these pages to your menu manually:\n")
    
    print("📋 Steps:")
    print("1. Log into WordPress Admin: https://mytribal.ai/wp-admin")
    print("2. Go to: Appearance → Menus")
    print("3. Select your main navigation menu (or create a new one)")
    print("4. In the left sidebar, find 'Pages' section")
    print("5. Check the boxes for these pages:")
    
    for slug, page_info in pages_map.items():
        page_title = page_info.get('title', {}).get('rendered', slug)
        page_id = page_info.get('id')
        print(f"   ☐ {page_title} (ID: {page_id}, slug: {slug})")
    
    print("\n6. Click 'Add to Menu' button")
    print("7. Drag and drop items to reorder if needed")
    print("8. Click 'Save Menu' button")
    print("\n" + "="*70)
    
    print("\n💡 TIP: For footer menu:")
    print("   - You can add these pages to a separate 'Footer Menu'")
    print("   - Most themes support multiple menu locations")
    print("   - Go to: Appearance → Menus → Manage Locations")


def check_menu_locations():
    """Check available menu locations in the theme."""
    try:
        headers = {
            'Authorization': create_auth_header(),
            'Content-Type': 'application/json',
        }
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Try to get menu locations
        url = f"{WP_URL}/wp-json/wp/v2/menu-locations"
        resp = requests.get(url, headers=headers, verify=False, timeout=30)
        
        if resp.status_code == 200:
            locations = resp.json()
            if locations:
                print("\n📍 Available menu locations:")
                for location, name in locations.items():
                    print(f"   - {location}: {name}")
                return True
        
        return False
    except Exception as e:
        return False


def main():
    print("🚀 Adding Pages to Navigation Menu")
    print("="*70)
    
    # Get the pages we need to add
    pages_map = get_pages()
    
    if not pages_map:
        print("❌ Could not find required pages. Make sure they're published.")
        return
    
    print(f"\n✅ Found {len(pages_map)} page(s) to add to menu")
    
    # Check menu locations
    check_menu_locations()
    
    # Try REST API approach (usually won't work without plugin)
    if not add_pages_to_menu_rest_api(pages_map):
        # Provide manual instructions
        print_manual_instructions(pages_map)
    
    print("\n✅ Instructions provided. Please add pages to menu manually.")
    print("   Once added, your site will meet AdSense navigation requirements!")


if __name__ == "__main__":
    main()


