#!/usr/bin/env python3
"""
Quick WordPress Posts Checker
Check what posts exist and their status
"""

import os
import ssl
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# WordPress configuration
WP_URL = os.getenv("WP_URL", "https://mytribal.ai").rstrip('/')
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

def check_wordpress_posts():
    """Check what posts exist on the WordPress site"""
    print("🔍 Checking WordPress Posts...")
    print(f"🌐 Site: {WP_URL}")
    print("=" * 50)
    
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Check posts via REST API
        posts_url = f"{WP_URL}/wp-json/wp/v2/posts?per_page=10&status=publish"
        print(f"📡 Checking: {posts_url}")
        
        response = requests.get(posts_url, verify=False, timeout=30)
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            posts = response.json()
            print(f"✅ Found {len(posts)} published posts")
            print("\n📝 Recent Posts:")
            print("-" * 30)
            
            for i, post in enumerate(posts, 1):
                print(f"{i}. {post.get('title', {}).get('rendered', 'No Title')}")
                print(f"   ID: {post.get('id')}")
                print(f"   Status: {post.get('status')}")
                print(f"   Date: {post.get('date')}")
                print(f"   URL: {post.get('link')}")
                print(f"   Categories: {[cat.get('name') for cat in post.get('categories', [])]}")
                print()
        else:
            print(f"❌ Failed to fetch posts: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Error checking posts: {e}")
    
    # Check pages too
    print("\n📄 Checking Pages...")
    print("-" * 30)
    
    try:
        pages_url = f"{WP_URL}/wp-json/wp/v2/pages?per_page=10&status=publish"
        response = requests.get(pages_url, verify=False, timeout=30)
        
        if response.status_code == 200:
            pages = response.json()
            print(f"✅ Found {len(pages)} published pages")
            
            for i, page in enumerate(pages, 1):
                print(f"{i}. {page.get('title', {}).get('rendered', 'No Title')}")
                print(f"   ID: {page.get('id')}")
                print(f"   Status: {page.get('status')}")
                print(f"   URL: {page.get('link')}")
                print()
        else:
            print(f"❌ Failed to fetch pages: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking pages: {e}")
    
    # Check categories
    print("\n🏷️ Checking Categories...")
    print("-" * 30)
    
    try:
        categories_url = f"{WP_URL}/wp-json/wp/v2/categories"
        response = requests.get(categories_url, verify=False, timeout=30)
        
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ Found {len(categories)} categories")
            
            for cat in categories:
                print(f"• {cat.get('name')} (ID: {cat.get('id')}) - {cat.get('count')} posts")
        else:
            print(f"❌ Failed to fetch categories: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking categories: {e}")

def check_specific_post(post_id):
    """Check a specific post by ID"""
    print(f"\n🔍 Checking Specific Post ID: {post_id}")
    print("-" * 40)
    
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        
        post_url = f"{WP_URL}/wp-json/wp/v2/posts/{post_id}"
        response = requests.get(post_url, verify=False, timeout=30)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            post = response.json()
            print(f"✅ Post found:")
            print(f"   Title: {post.get('title', {}).get('rendered', 'No Title')}")
            print(f"   Status: {post.get('status')}")
            print(f"   Date: {post.get('date')}")
            print(f"   URL: {post.get('link')}")
            print(f"   Content length: {len(post.get('content', {}).get('rendered', ''))} characters")
            print(f"   Categories: {post.get('categories')}")
        else:
            print(f"❌ Post not found: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Error checking post: {e}")

def main():
    """Main function"""
    check_wordpress_posts()
    
    # Check the specific post that was created (ID 93)
    check_specific_post(93)
    
    print("\n" + "=" * 50)
    print("🎯 DIAGNOSTIC COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    main()
