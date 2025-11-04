#!/usr/bin/env python3
"""
Check content quality issues that might cause AdSense "Low value content" rejection.
"""

import requests
from bs4 import BeautifulSoup
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WP_URL = "https://mytribal.ai"

def analyze_post(url):
    """Analyze a single post for quality indicators."""
    try:
        resp = requests.get(url, verify=False, timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Get main content
            article = soup.find('article') or soup.find('main') or soup.find('div', class_=lambda x: x and ('content' in str(x).lower() or 'post' in str(x).lower()))
            
            if not article:
                return None
            
            text = article.get_text()
            
            # Count words
            words = text.split()
            word_count = len(words)
            
            # Check for headings
            headings = len(soup.find_all(['h1', 'h2', 'h3', 'h4']))
            
            # Check for images
            images = len(soup.find_all('img'))
            
            # Check for links
            links = len(soup.find_all('a', href=True))
            
            # Check for paragraphs
            paragraphs = len(soup.find_all('p'))
            
            # Check for AI-generated indicators (common phrases)
            ai_phrases = [
                'as an ai', 'i am an ai', 'i cannot', 'i don\'t have',
                'as a large language model', 'i\'m designed to',
                'i\'m an ai assistant', 'i don\'t have personal'
            ]
            has_ai_phrases = any(phrase.lower() in text.lower() for phrase in ai_phrases)
            
            return {
                'word_count': word_count,
                'headings': headings,
                'images': images,
                'links': links,
                'paragraphs': paragraphs,
                'has_ai_phrases': has_ai_phrases
            }
    except:
        return None

def get_recent_posts():
    """Get recent posts from the homepage."""
    try:
        resp = requests.get(WP_URL, verify=False, timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Find post links
            links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                text = link.get_text().strip()
                
                # Filter for post URLs (not pages, not external)
                if '/wp-admin' not in href and '#' not in href:
                    if any(word in text.lower() for word in ['unlock', 'ai', 'insights', 'trending']) or len(text) > 30:
                        if href.startswith('/') or 'mytribal.ai' in href:
                            full_url = href if href.startswith('http') else f"{WP_URL}{href}"
                            if full_url not in links and 'page' not in href.lower():
                                links.append(full_url)
            
            return links[:10]  # Check first 10
    except:
        return []

def check_content_issues():
    """Main content quality check."""
    print("="*70)
    print("CONTENT QUALITY CHECK FOR ADSENSE")
    print("="*70)
    
    print("\n🔍 Checking your site's content quality...")
    
    posts = get_recent_posts()
    
    if not posts:
        print("⚠️ Could not automatically detect posts.")
        print("\n📋 Manual Checklist:")
        print("   1. Visit your site and check your posts")
        print("   2. Verify each post has:")
        print("      - At least 500-800 words")
        print("      - Unique, original content")
        print("      - Proper headings (H2, H3)")
        print("      - Images or media")
        print("      - Internal/external links")
        print("      - No AI disclaimers")
        return
    
    print(f"\n✅ Found {len(posts)} recent posts to analyze\n")
    
    quality_issues = []
    good_posts = 0
    
    for i, post_url in enumerate(posts[:5], 1):  # Check first 5
        print(f"Analyzing post {i}...")
        analysis = analyze_post(post_url)
        
        if analysis:
            issues = []
            
            if analysis['word_count'] < 300:
                issues.append(f"❌ Too short ({analysis['word_count']} words, need 500+)")
            elif analysis['word_count'] < 500:
                issues.append(f"⚠️ Short ({analysis['word_count']} words, aim for 500+)")
            else:
                print(f"   ✅ Length: {analysis['word_count']} words")
            
            if analysis['headings'] < 2:
                issues.append(f"⚠️ Need more headings (only {analysis['headings']} found)")
            
            if analysis['images'] == 0:
                issues.append("⚠️ No images found")
            
            if analysis['has_ai_phrases']:
                issues.append("❌ Contains AI disclaimer phrases - REMOVE THESE!")
            
            if analysis['paragraphs'] < 5:
                issues.append(f"⚠️ Need more paragraphs (only {analysis['paragraphs']} found)")
            
            if issues:
                quality_issues.extend(issues)
                print(f"   Issues found:")
                for issue in issues:
                    print(f"      {issue}")
            else:
                good_posts += 1
                print(f"   ✅ Quality looks good!")
    
    print("\n" + "="*70)
    print("RECOMMENDATIONS TO FIX 'LOW VALUE CONTENT' REJECTION")
    print("="*70)
    
    print("\n📝 CONTENT QUALITY IMPROVEMENTS:")
    print("\n1. ✅ POST LENGTH:")
    print("   - Each post should be 500-800+ words minimum")
    print("   - AdSense prefers substantial, in-depth content")
    print("   - Your daily automation posts may be too short")
    
    print("\n2. ✅ UNIQUE VALUE:")
    print("   - Add your own analysis and insights to each post")
    print("   - Don't just aggregate RSS content - add commentary")
    print("   - Include your expertise and opinions")
    print("   - Add personal perspective or case studies")
    
    print("\n3. ✅ STRUCTURE & FORMATTING:")
    print("   - Use clear headings (H2, H3) to organize content")
    print("   - Break content into readable paragraphs")
    print("   - Add bullet points or lists where appropriate")
    print("   - Include images, charts, or visual elements")
    
    print("\n4. ✅ REMOVE AI DISCLAIMERS:")
    print("   - Remove phrases like 'As an AI', 'I am an AI'")
    print("   - Don't mention AI limitations")
    print("   - Write in first person or third person")
    print("   - Make content sound human-written")
    
    print("\n5. ✅ ADD DEPTH:")
    print("   - Go beyond summaries - add analysis")
    print("   - Include expert opinions or quotes")
    print("   - Add context and background information")
    print("   - Link to related topics for further reading")
    
    print("\n6. ✅ ENGAGEMENT ELEMENTS:")
    print("   - Add call-to-action questions")
    print("   - Include reader engagement prompts")
    print("   - Add comments section if possible")
    print("   - Internal linking between related posts")
    
    print("\n" + "="*70)
    print("IMMEDIATE ACTION ITEMS")
    print("="*70)
    
    print("\n🔧 BEFORE RESUBMITTING:")
    print("   1. Review your recent posts (last 10-15)")
    print("   2. Expand shorter posts to 500+ words")
    print("   3. Add original analysis to each post")
    print("   4. Remove any AI disclaimer language")
    print("   5. Add more headings and structure")
    print("   6. Include images/media where relevant")
    print("   7. Add internal links between related posts")
    
    print("\n⏱️ TIMELINE:")
    print("   - Fix content issues (1-2 days)")
    print("   - Publish 5-10 improved posts")
    print("   - Wait 1-2 weeks after improvements")
    print("   - Then request review again")
    
    print("\n📚 RESOURCES:")
    print("   - AdSense Content Policies: https://support.google.com/adsense/answer/1348688")
    print("   - Quality Guidelines: https://developers.google.com/search/docs/essentials/spam-policies")
    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("❌ Missing packages. Install with: pip install requests beautifulsoup4")
        exit(1)
    
    check_content_issues()

