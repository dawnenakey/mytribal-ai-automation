#!/usr/bin/env python3
"""
Check the actual navigation structure on the website.
"""

import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL = "https://mytribal.ai"

def check_navigation():
    try:
        print("🔍 Checking homepage navigation structure...\n")
        response = requests.get(WP_URL, verify=False, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all navigation elements
            navs = soup.find_all(['nav', 'header'])
            
            print("="*70)
            print("NAVIGATION ELEMENTS FOUND")
            print("="*70)
            
            if navs:
                for i, nav in enumerate(navs, 1):
                    print(f"\n📍 Navigation Element #{i}:")
                    print(f"   Tag: {nav.name}")
                    print(f"   Classes: {nav.get('class', [])}")
                    print(f"   ID: {nav.get('id', 'None')}")
                    
                    # Find all links in this nav
                    links = nav.find_all('a', href=True)
                    if links:
                        print(f"   Links found: {len(links)}")
                        for link in links:
                            text = link.get_text().strip()
                            href = link.get('href', '')
                            if text:  # Only show links with text
                                print(f"      - '{text}' → {href}")
                    else:
                        print(f"   No links found in this navigation")
            else:
                print("⚠️ No <nav> or <header> elements found")
            
            # Check for common menu structures
            print("\n" + "="*70)
            print("SEARCHING FOR MENU STRUCTURES")
            print("="*70)
            
            # Common menu class names
            menu_selectors = [
                'menu',
                'navigation',
                'nav-menu',
                'main-menu',
                'primary-menu',
                'header-menu',
                'site-navigation',
                'main-navigation'
            ]
            
            for selector in menu_selectors:
                menus = soup.find_all(class_=lambda x: x and selector in ' '.join(x).lower())
                if menus:
                    print(f"\n✅ Found elements with '{selector}' class:")
                    for menu in menus:
                        links = menu.find_all('a', href=True)
                        if links:
                            print(f"   Links:")
                            for link in links:
                                text = link.get_text().strip()
                                href = link.get('href', '')
                                if text:
                                    print(f"      - '{text}' → {href}")
            
            # Check header area specifically
            print("\n" + "="*70)
            print("HEADER AREA ANALYSIS")
            print("="*70)
            
            header = soup.find('header')
            if header:
                print("✅ <header> tag found")
                header_links = header.find_all('a', href=True)
                if header_links:
                    print(f"   Links in header: {len(header_links)}")
                    for link in header_links[:10]:  # Show first 10
                        text = link.get_text().strip()
                        href = link.get('href', '')
                        if text:
                            print(f"      - '{text}' → {href}")
            else:
                print("⚠️ No <header> tag found")
            
            # Check for WordPress menu
            wp_menus = soup.find_all(id=lambda x: x and 'menu' in str(x).lower())
            if wp_menus:
                print(f"\n✅ Found WordPress menu elements:")
                for menu in wp_menus:
                    print(f"   ID: {menu.get('id')}")
                    links = menu.find_all('a', href=True)
                    if links:
                        for link in links:
                            text = link.get_text().strip()
                            if text:
                                print(f"      - '{text}'")
            
            print("\n" + "="*70)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_navigation()


