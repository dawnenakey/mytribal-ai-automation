#!/usr/bin/env python3
"""
WordPress Redirect Diagnostic Tool
Helps diagnose and fix privacy policy and legal page redirect issues
"""

import os
import json
import base64
import ssl
import requests
from dotenv import load_dotenv
import urllib3
from urllib.parse import urljoin, urlparse

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
load_dotenv()

# WordPress configuration
WP_URL = os.getenv("WP_URL", "https://mytribal.ai").rstrip('/')
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

def create_auth_header():
    """Create Basic Auth header for WordPress REST API"""
    if not WP_USERNAME or not WP_APP_PASSWORD:
        return None
    
    credentials = f"{WP_USERNAME}:{WP_APP_PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded_credentials}"

def check_page_exists(page_slug):
    """Check if a page exists and get its details"""
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Try to get the page by slug
        api_url = f"{WP_URL}/wp-json/wp/v2/pages?slug={page_slug}"
        response = requests.get(api_url, verify=False, timeout=30)
        
        if response.status_code == 200:
            pages = response.json()
            if pages:
                page = pages[0]
                return {
                    'exists': True,
                    'id': page['id'],
                    'title': page['title']['rendered'],
                    'status': page['status'],
                    'link': page['link'],
                    'slug': page['slug']
                }
        
        return {'exists': False}
        
    except Exception as e:
        print(f"❌ Error checking page {page_slug}: {e}")
        return {'exists': False, 'error': str(e)}

def check_redirects(url_path):
    """Check if a URL path redirects and where it goes"""
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        
        full_url = urljoin(WP_URL, url_path)
        print(f"🔍 Testing redirect for: {full_url}")
        
        # Follow redirects to see where it goes
        response = requests.get(full_url, verify=False, allow_redirects=True, timeout=30)
        
        final_url = response.url
        redirect_count = len(response.history)
        
        print(f"📊 Final URL: {final_url}")
        print(f"🔄 Redirects followed: {redirect_count}")
        
        if redirect_count > 0:
            print("📋 Redirect chain:")
            for i, resp in enumerate(response.history):
                print(f"   {i+1}. {resp.url} → {resp.status_code}")
            print(f"   Final: {final_url} → {response.status_code}")
        
        return {
            'original_url': full_url,
            'final_url': final_url,
            'redirect_count': redirect_count,
            'status_code': response.status_code,
            'is_redirected': redirect_count > 0
        }
        
    except Exception as e:
        print(f"❌ Error checking redirects: {e}")
        return None

def check_wordpress_settings():
    """Check WordPress settings that might affect redirects"""
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        
        auth_header = create_auth_header()
        if not auth_header:
            print("⚠️ No WordPress credentials - can't check settings")
            return None
        
        headers = {
            'Authorization': auth_header,
            'Content-Type': 'application/json'
        }
        
        # Check site settings
        settings_url = f"{WP_URL}/wp-json/wp/v2/settings"
        response = requests.get(settings_url, headers=headers, verify=False, timeout=30)
        
        if response.status_code == 200:
            settings = response.json()
            return {
                'site_title': settings.get('title'),
                'site_description': settings.get('description'),
                'url': settings.get('url'),
                'home': settings.get('home')
            }
        
        return None
        
    except Exception as e:
        print(f"❌ Error checking WordPress settings: {e}")
        return None

def check_htaccess():
    """Check if .htaccess file exists and might contain redirect rules"""
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        
        htaccess_url = urljoin(WP_URL, '.htaccess')
        response = requests.get(htaccess_url, verify=False, timeout=30)
        
        if response.status_code == 200:
            content = response.text
            print("📄 .htaccess file found")
            
            # Look for common redirect patterns
            redirect_patterns = [
                'RewriteRule',
                'Redirect',
                'RedirectMatch',
                'RewriteCond'
            ]
            
            found_patterns = []
            for pattern in redirect_patterns:
                if pattern in content:
                    found_patterns.append(pattern)
            
            if found_patterns:
                print(f"⚠️ Found redirect patterns in .htaccess: {', '.join(found_patterns)}")
                print("   This might be causing your redirect issues")
            else:
                print("✅ No obvious redirect patterns found in .htaccess")
            
            return True
        else:
            print("ℹ️ .htaccess file not accessible or doesn't exist")
            return False
            
    except Exception as e:
        print(f"❌ Error checking .htaccess: {e}")
        return False

def create_privacy_policy_page():
    """Create a privacy policy page if it doesn't exist"""
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        
        auth_header = create_auth_header()
        if not auth_header:
            print("❌ WordPress credentials not available")
            return False
        
        # Check if privacy policy already exists
        existing = check_page_exists('privacy-policy')
        if existing['exists']:
            print(f"✅ Privacy Policy page already exists (ID: {existing['id']})")
            return True
        
        # Create new privacy policy page
        headers = {
            'Authorization': auth_header,
            'Content-Type': 'application/json'
        }
        
        page_data = {
            'title': 'Privacy Policy',
            'content': '''
            <h2>Privacy Policy</h2>
            <p>This is a placeholder privacy policy page. Please update with your actual privacy policy content.</p>
            <h3>Information We Collect</h3>
            <p>We collect information you provide directly to us when you use our services.</p>
            <h3>How We Use Your Information</h3>
            <p>We use the information we collect to provide, maintain, and improve our services.</p>
            <h3>Contact Us</h3>
            <p>If you have any questions about this Privacy Policy, please contact us.</p>
            ''',
            'status': 'publish',
            'slug': 'privacy-policy'
        }
        
        api_url = f"{WP_URL}/wp-json/wp/v2/pages"
        response = requests.post(api_url, headers=headers, data=json.dumps(page_data), verify=False, timeout=60)
        
        if response.status_code == 201:
            new_page = response.json()
            print(f"✅ Created Privacy Policy page (ID: {new_page['id']})")
            print(f"   URL: {new_page['link']}")
            return True
        else:
            print(f"❌ Failed to create Privacy Policy page: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error creating privacy policy page: {e}")
        return False

def diagnose_privacy_policy_redirects():
    """Main diagnostic function"""
    print("🔍 WordPress Privacy Policy Redirect Diagnostic")
    print("=" * 60)
    print(f"🌐 Site: {WP_URL}")
    print("=" * 60)
    
    # Check WordPress settings
    print("\n📋 Checking WordPress Settings...")
    settings = check_wordpress_settings()
    if settings:
        print(f"   Site Title: {settings.get('site_title', 'N/A')}")
        print(f"   Site URL: {settings.get('url', 'N/A')}")
        print(f"   Home URL: {settings.get('home', 'N/A')}")
    
    # Check .htaccess for redirect rules
    print("\n📄 Checking .htaccess file...")
    check_htaccess()
    
    # Check if privacy policy page exists
    print("\n📝 Checking Privacy Policy Page...")
    privacy_page = check_page_exists('privacy-policy')
    if privacy_page['exists']:
        print(f"✅ Privacy Policy page exists:")
        print(f"   ID: {privacy_page['id']}")
        print(f"   Title: {privacy_page['title']}")
        print(f"   Status: {privacy_page['status']}")
        print(f"   URL: {privacy_page['link']}")
    else:
        print("❌ Privacy Policy page not found")
        print("   This could be why you're getting redirects")
    
    # Check common privacy policy URLs for redirects
    print("\n🔄 Testing Privacy Policy URLs for Redirects...")
    privacy_urls = [
        '/privacy-policy/',
        '/privacy/',
        '/legal/privacy-policy/',
        '/privacy-policy',
        '/legal/'
    ]
    
    for url_path in privacy_urls:
        print(f"\n--- Testing: {url_path} ---")
        redirect_info = check_redirects(url_path)
        if redirect_info and redirect_info['is_redirected']:
            print(f"⚠️ REDIRECT DETECTED: {url_path} → {redirect_info['final_url']}")
    
    # Check if we need to create a privacy policy page
    if not privacy_page['exists']:
        print("\n🔧 Creating Privacy Policy Page...")
        if create_privacy_policy_page():
            print("✅ Privacy Policy page created successfully")
            print("   Test the URL now to see if redirects are fixed")
        else:
            print("❌ Failed to create Privacy Policy page")
    
    print("\n" + "=" * 60)
    print("🎯 DIAGNOSTIC COMPLETE")
    print("=" * 60)
    
    # Summary and recommendations
    print("\n📋 SUMMARY & RECOMMENDATIONS:")
    print("1. If Privacy Policy page was missing, it has been created")
    print("2. Check your WordPress theme's header/footer for privacy policy links")
    print("3. Verify your theme's navigation menu settings")
    print("4. Check for any redirect plugins that might be interfering")
    print("5. Test the privacy policy URL: {WP_URL}/privacy-policy/")

def main():
    """Main function"""
    if not WP_URL:
        print("❌ WP_URL not found in environment variables")
        print("   Please set WP_URL in your .env file")
        return
    
    diagnose_privacy_policy_redirects()

if __name__ == "__main__":
    main()
