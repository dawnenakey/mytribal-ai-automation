#!/usr/bin/env python3
"""
Helper script to add pages to WordPress main navigation menu.
Provides detailed instructions and attempts alternative methods.
"""

import os
import json
import base64
import ssl
import requests
from dotenv import load_dotenv
import urllib3

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL = os.getenv("WP_URL", "https://mytribal.ai").rstrip('/')
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")


def create_auth_header():
    if not WP_USERNAME or not WP_APP_PASSWORD:
        return None
    credentials = f"{WP_USERNAME}:{WP_APP_PASSWORD}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


def get_page_info():
    """Get information about pages we want to add."""
    headers = {
        'Authorization': create_auth_header(),
        'Content-Type': 'application/json',
    }
    ssl._create_default_https_context = ssl._create_unverified_context
    
    pages_to_add = [
        {'slug': 'services', 'title': 'Services'},
        {'slug': 'case-studies', 'title': 'Case Studies'},
        {'slug': 'about', 'title': 'About Us'},
        {'slug': 'contact', 'title': 'Contact'},
    ]
    
    pages_info = []
    for page_data in pages_to_add:
        url = f"{WP_URL}/wp-json/wp/v2/pages?slug={page_data['slug']}"
        resp = requests.get(url, headers=headers, verify=False, timeout=30)
        if resp.status_code == 200:
            pages = resp.json()
            if pages:
                pages_info.append({
                    'id': pages[0]['id'],
                    'title': pages[0]['title']['rendered'],
                    'slug': page_data['slug'],
                    'url': pages[0]['link']
                })
    
    return pages_info


def print_detailed_instructions(pages_info):
    """Print step-by-step instructions."""
    print("\n" + "="*70)
    print("STEP-BY-STEP: Add Pages to Main Navigation Menu")
    print("="*70)
    
    print("\n📋 Pages to add:")
    for i, page in enumerate(pages_info, 1):
        print(f"   {i}. {page['title']} (ID: {page['id']})")
    
    print("\n" + "-"*70)
    print("STEP 1: Access WordPress Admin")
    print("-"*70)
    print("1. Open your browser")
    print(f"2. Go to: {WP_URL}/wp-admin")
    print("3. Log in with your WordPress credentials")
    
    print("\n" + "-"*70)
    print("STEP 2: Navigate to Menus")
    print("-"*70)
    print("1. In the left sidebar, hover over 'Appearance'")
    print("2. Click on 'Menus'")
    print("   (Alternatively: Appearance → Menus)")
    
    print("\n" + "-"*70)
    print("STEP 3: Select or Create Menu")
    print("-"*70)
    print("1. At the top, you'll see 'Select a menu to edit:'")
    print("2. Choose your main navigation menu from the dropdown")
    print("   (Common names: 'Primary Menu', 'Main Menu', 'Header Menu', or 'Navigation')")
    print("3. If no menu exists, click 'create a new menu' link")
    print("   - Enter name: 'Main Menu' or 'Primary Menu'")
    print("   - Click 'Create Menu' button")
    
    print("\n" + "-"*70)
    print("STEP 4: Add Pages to Menu")
    print("-"*70)
    print("1. In the left column, find the 'Pages' section")
    print("2. If you don't see it, click the 'View All' tab at the top of Pages section")
    print("3. Look for these pages and check the boxes:")
    
    for page in pages_info:
        print(f"   ☐ {page['title']}")
    
    print("\n4. Click the 'Add to Menu' button")
    print("   (This button is below the list of pages)")
    
    print("\n" + "-"*70)
    print("STEP 5: Organize Menu Items")
    print("-"*70)
    print("1. In the right column, you'll see your menu structure")
    print("2. Drag and drop menu items to reorder them")
    print("3. Recommended order:")
    print("   - Home (if exists)")
    print("   - Services")
    print("   - Case Studies")
    print("   - About Us")
    print("   - Contact")
    
    print("\n4. To create submenus (optional):")
    print("   - Drag an item slightly to the right under another item")
    print("   - It will become a submenu item")
    
    print("\n" + "-"*70)
    print("STEP 6: Set Menu Location (IMPORTANT)")
    print("-"*70)
    print("1. Scroll down to 'Menu Settings' at the bottom")
    print("2. Under 'Display location', check the box for:")
    print("   ☐ Primary Menu")
    print("   ☐ Main Navigation")
    print("   ☐ Header Menu")
    print("   (The exact name depends on your theme)")
    print("3. If you see multiple options, check 'Primary' or 'Main'")
    
    print("\n" + "-"*70)
    print("STEP 7: Save Menu")
    print("-"*70)
    print("1. Click the 'Save Menu' button (top right of menu structure)")
    print("2. You should see a success message: 'Menu has been saved'")
    
    print("\n" + "-"*70)
    print("STEP 8: Verify")
    print("-"*70)
    print("1. Visit your website: https://mytribal.ai")
    print("2. Check the main navigation menu at the top")
    print("3. You should see: Services, Case Studies, About Us, Contact")
    
    print("\n" + "="*70)
    print("TROUBLESHOOTING")
    print("="*70)
    print("\n❓ Pages not showing in 'Pages' section?")
    print("   - Click 'View All' tab")
    print("   - Use the search box to find pages by name")
    print("   - Make sure pages are published (not drafts)")
    
    print("\n❓ Menu not appearing on website?")
    print("   - Make sure you checked a menu location in Step 6")
    print("   - Try different location options")
    print("   - Some themes have custom menu locations")
    
    print("\n❓ Can't find 'Menus' option?")
    print("   - Some themes hide it under: Appearance → Customize → Menus")
    print("   - Or try: Appearance → Theme Options → Menus")
    
    print("\n" + "="*70)
    print("\n✅ Once complete, your site will be ready for AdSense!")


def print_quick_reference(pages_info):
    """Print a quick reference card."""
    print("\n" + "="*70)
    print("QUICK REFERENCE CARD")
    print("="*70)
    print("\n🔗 Direct Links:")
    print(f"   Admin: {WP_URL}/wp-admin")
    print(f"   Menus: {WP_URL}/wp-admin/nav-menus.php")
    print("\n📄 Pages to Add (check these boxes):")
    for page in pages_info:
        print(f"   ☐ {page['title']}")
    print("\n✅ After adding, check menu location: Primary/Main Menu")
    print("="*70)


def main():
    print("🚀 WordPress Navigation Menu Helper")
    print("="*70)
    
    pages_info = get_page_info()
    
    if not pages_info:
        print("❌ Could not retrieve page information.")
        print("   Make sure pages are published and WordPress credentials are correct.")
        return
    
    print(f"\n✅ Found {len(pages_info)} page(s) ready to add:")
    for page in pages_info:
        print(f"   - {page['title']} ({page['url']})")
    
    print_detailed_instructions(pages_info)
    print_quick_reference(pages_info)
    
    print("\n💡 TIP: Keep this terminal open while following the steps!")
    print("   You can reference the instructions above anytime.\n")


if __name__ == "__main__":
    main()


