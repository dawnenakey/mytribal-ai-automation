#!/usr/bin/env python3
"""
Check what pages are visible on the website.
Scrapes the live site to verify pages exist and are accessible.
"""

import requests
from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL = "https://mytribal.ai"

# Pages to check
PAGES_TO_CHECK = [
    "/",
    "/services/",
    "/case-studies/",
    "/privacy-policy/",
    "/about/",
    "/contact/",
]

def check_page(url):
    """Check if a page exists and is accessible."""
    try:
        full_url = urljoin(WP_URL, url)
        print(f"\n🔍 Checking: {full_url}")
        
        response = requests.get(full_url, verify=False, timeout=15, allow_redirects=True)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get page title
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else "No title found"
            
            # Check for main content
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=lambda x: x and ('content' in x.lower() or 'page' in x.lower()))
            
            # Get h1 heading
            h1 = soup.find('h1')
            h1_text = h1.get_text().strip() if h1 else "No H1 found"
            
            # Check if page appears to have content
            text_content = soup.get_text()
            word_count = len(text_content.split())
            
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📄 Title: {title}")
            print(f"   📝 H1: {h1_text}")
            print(f"   📊 Content length: ~{word_count} words")
            
            # Check for navigation menu
            nav = soup.find('nav')
            if nav:
                nav_links = [a.get_text().strip() for a in nav.find_all('a')]
                print(f"   🔗 Navigation links found: {len(nav_links)}")
                if nav_links:
                    print(f"      Sample: {', '.join(nav_links[:5])}")
            
            # Check for footer
            footer = soup.find('footer')
            if footer:
                footer_links = [a.get_text().strip() for a in footer.find_all('a')]
                print(f"   👣 Footer links found: {len(footer_links)}")
            
            # Check for specific content indicators
            if "privacy" in url.lower():
                if "cookie" in text_content.lower() or "data" in text_content.lower():
                    print(f"   ✅ Privacy policy content detected")
            
            if "about" in url.lower():
                if "mytribal" in text_content.lower() or "data science" in text_content.lower():
                    print(f"   ✅ About page content detected")
            
            if "contact" in url.lower():
                if "admin@mytribal.ai" in text_content or "email" in text_content.lower():
                    print(f"   ✅ Contact information detected")
            
            return True, title, h1_text, word_count
            
        elif response.status_code == 404:
            print(f"   ❌ Status: 404 (Page Not Found)")
            return False, None, None, 0
        else:
            print(f"   ⚠️ Status: {response.status_code}")
            return False, None, None, 0
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        return False, None, None, 0
    except Exception as e:
        print(f"   ❌ Unexpected error: {str(e)[:100]}")
        return False, None, None, 0


def check_homepage_links():
    """Check what links are present on the homepage."""
    try:
        print(f"\n🏠 Checking homepage links...")
        response = requests.get(WP_URL, verify=False, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all links
            links = soup.find_all('a', href=True)
            important_pages = {}
            
            for link in links:
                href = link.get('href', '')
                text = link.get_text().strip()
                
                # Check for our important pages
                for page in ['services', 'case-studies', 'privacy', 'about', 'contact']:
                    if page in href.lower():
                        if page not in important_pages:
                            important_pages[page] = []
                        important_pages[page].append(text or href)
            
            if important_pages:
                print(f"   ✅ Found links to important pages:")
                for page, links_list in important_pages.items():
                    unique_links = list(set(links_list))[:3]  # Show first 3 unique
                    print(f"      - {page}: {', '.join(unique_links)}")
            else:
                print(f"   ⚠️ No links to important pages found on homepage")
            
    except Exception as e:
        print(f"   ❌ Error checking homepage: {str(e)[:100]}")


def main():
    print("="*70)
    print("WEBSITE PAGE CHECKER")
    print("="*70)
    print(f"Checking: {WP_URL}\n")
    
    results = []
    
    # Check each page
    for page in PAGES_TO_CHECK:
        success, title, h1, word_count = check_page(page)
        results.append({
            'page': page,
            'success': success,
            'title': title,
            'h1': h1,
            'word_count': word_count
        })
    
    # Check homepage links
    check_homepage_links()
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"\n✅ Accessible pages: {len(successful)}/{len(results)}")
    for result in successful:
        print(f"   - {result['page']}: {result['h1'] or result['title']}")
    
    if failed:
        print(f"\n❌ Failed pages: {len(failed)}")
        for result in failed:
            print(f"   - {result['page']}")
    
    print("\n" + "="*70)
    
    # AdSense readiness check
    print("\n📋 AdSense Readiness Check:")
    required_pages = ['/privacy-policy/', '/about/', '/contact/']
    found_required = all(any(r['page'] == p and r['success'] for r in results) for p in required_pages)
    
    if found_required:
        print("   ✅ All required pages (Privacy Policy, About, Contact) are accessible")
    else:
        print("   ⚠️ Some required pages are missing or not accessible")
    
    homepage_success = any(r['page'] == '/' and r['success'] for r in results)
    if homepage_success:
        print("   ✅ Homepage is accessible")
    else:
        print("   ⚠️ Homepage check failed")


if __name__ == "__main__":
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("❌ Missing required packages. Install with:")
        print("   pip install requests beautifulsoup4")
        exit(1)
    
    main()


