#!/usr/bin/env python3
"""
Daily Content and Social Media Generator for MyTribal.AI
Generates daily blog posts and social media content for X, Instagram, and LinkedIn
"""

import os
import json
import base64
import ssl
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
import urllib3
import random

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
load_dotenv()

# WordPress configuration
WP_URL = os.getenv("WP_URL", "https://mytribal.ai").rstrip('/')
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# RSS feeds for daily content
DAILY_RSS_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://venturebeat.com/feed/",
    "https://artificialintelligence-news.com/feed/",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "https://www.reddit.com/r/artificial/hot.rss?limit=5",
    "https://news.ycombinator.com/rss"
]

def create_auth_header():
    """Create Basic Auth header for WordPress REST API"""
    if not WP_USERNAME or not WP_APP_PASSWORD:
        return None
    
    credentials = f"{WP_USERNAME}:{WP_APP_PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded_credentials}"

def get_or_create_category(category_name):
    """Get existing category or create new one"""
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        
        auth_header = create_auth_header()
        headers = {
            'Authorization': auth_header,
            'Content-Type': 'application/json'
        }
        
        # Search for existing category
        search_url = f"{WP_URL}/wp-json/wp/v2/categories?search={category_name}"
        response = requests.get(search_url, headers=headers, verify=False)
        
        if response.status_code == 200:
            categories = response.json()
            for cat in categories:
                if cat.get('name', '').lower() == category_name.lower():
                    print(f"✅ Using existing category: {category_name} (ID: {cat['id']})")
                    return cat['id']
        
        # Create new category
        create_url = f"{WP_URL}/wp-json/wp/v2/categories"
        category_data = {
            'name': category_name,
            'slug': category_name.lower().replace(' ', '-'),
            'description': f'Content related to {category_name}'
        }
        
        response = requests.post(create_url, headers=headers, data=json.dumps(category_data), verify=False)
        
        if response.status_code == 201:
            new_category = response.json()
            print(f"✅ Created new category: {category_name} (ID: {new_category['id']})")
            return new_category['id']
        else:
            print(f"⚠️ Failed to create category, using default (ID: 1)")
            return 1
            
    except Exception as e:
        print(f"⚠️ Error managing categories: {e}, using default (ID: 1)")
        return 1

def fetch_trending_topics():
    """Fetch trending topics from RSS feeds"""
    print("📡 Fetching trending topics from RSS feeds...")
    
    all_entries = []
    
    for feed_url in DAILY_RSS_FEEDS:
        try:
            response = requests.get(feed_url, timeout=30)
            if response.status_code == 200:
                # Simple RSS parsing
                content = response.text
                
                # Extract titles (basic parsing)
                import re
                titles = re.findall(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE)
                
                for title in titles[:3]:  # Take first 3 titles from each feed
                    if title and len(title) > 20 and not title.startswith('<?xml'):
                        all_entries.append({
                            'title': title.strip(),
                            'source': feed_url.split('/')[2],  # Extract domain
                            'feed': feed_url
                        })
                
                print(f"✅ Fetched from {feed_url.split('/')[2]}")
                
        except Exception as e:
            print(f"⚠️ Error fetching {feed_url}: {e}")
            continue
    
    # Remove duplicates and select top topics
    unique_entries = []
    seen_titles = set()
    
    for entry in all_entries:
        title_lower = entry['title'].lower()
        if title_lower not in seen_titles and len(unique_entries) < 5:
            unique_entries.append(entry)
            seen_titles.add(title_lower)
    
    print(f"📊 Found {len(unique_entries)} unique trending topics")
    return unique_entries

def generate_daily_article(topics):
    """Generate a daily article based on trending topics"""
    if not OPENAI_API_KEY:
        print("❌ OpenAI API key not found")
        return None
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Create a summary of trending topics
        topics_summary = "\n".join([f"- {topic['title']} (via {topic['source']})" for topic in topics[:3]])
        
        prompt = f"""
        Create a compelling daily blog post titled "Today's AI & Tech Roundup" that covers these trending topics:
        
        {topics_summary}
        
        Requirements:
        - Write in an engaging, informative style
        - Connect the topics to AI and technology trends
        - Include insights about what these developments mean
        - Keep it around 400-600 words
        - Make it suitable for MyTribal.AI audience
        - Include a call-to-action encouraging readers to stay updated
        
        Format the response as clean HTML with <p> tags for paragraphs, <h3> for subheadings.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a tech writer specializing in AI and technology trends. Write engaging content that helps readers understand the latest developments in the tech world."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        article = response.choices[0].message.content.strip()
        print("✅ Daily article generated successfully")
        return article
        
    except Exception as e:
        print(f"❌ Error generating article: {e}")
        return None

def generate_social_media_posts(article_content, topics):
    """Generate social media posts for X, Instagram, and LinkedIn"""
    if not OPENAI_API_KEY:
        print("❌ OpenAI API key not found")
        return None
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Extract key points from the article
        key_points = "\n".join([f"- {topic['title']}" for topic in topics[:3]])
        
        prompt = f"""
        Create engaging social media posts for these platforms based on this content:
        
        Key Topics:
        {key_points}
        
        Article Summary: {article_content[:200]}...
        
        Create 3 different posts:
        
        1. X (Twitter) - 280 characters max, engaging, use hashtags #AI #Tech #Innovation
        2. Instagram - 2200 characters max, engaging, use emojis, hashtags #AI #Technology #Innovation #TechNews
        3. LinkedIn - Professional tone, 1300 characters max, business-focused, hashtags #AI #Technology #Innovation #TechTrends
        
        Format as JSON with keys: "x", "instagram", "linkedin"
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a social media expert specializing in tech content. Create engaging posts for different platforms with appropriate tone and length."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.8
        )
        
        try:
            posts = json.loads(response.choices[0].message.content.strip())
            print("✅ Social media posts generated successfully")
            return posts
        except json.JSONDecodeError:
            print("⚠️ Failed to parse JSON, creating manual posts")
            return create_manual_social_posts(topics)
        
    except Exception as e:
        print(f"❌ Error generating social posts: {e}")
        return create_manual_social_posts(topics)

def create_manual_social_posts(topics):
    """Create social media posts manually if AI generation fails"""
    print("🔧 Creating manual social media posts...")
    
    # X (Twitter) post
    x_post = f"🚀 Today's AI & Tech Roundup:\n\n"
    for i, topic in enumerate(topics[:2], 1):
        x_post += f"{i}. {topic['title'][:50]}...\n"
    x_post += "\n#AI #Tech #Innovation #TechNews"
    
    # Instagram post
    instagram_post = f"🤖 Today's AI & Tech Roundup 📱\n\n"
    for i, topic in enumerate(topics[:3], 1):
        instagram_post += f"🔹 {topic['title']}\n"
    instagram_post += f"\n💡 Stay ahead of the curve with the latest tech developments!\n\n"
    instagram_post += f"#AI #Technology #Innovation #TechNews #ArtificialIntelligence #TechTrends #Innovation #FutureTech"
    
    # LinkedIn post
    linkedin_post = f"📊 Today's AI & Technology Insights\n\n"
    for i, topic in enumerate(topics[:3], 1):
        linkedin_post += f"• {topic['title']}\n"
    linkedin_post += f"\nThese developments highlight the rapid pace of innovation in AI and technology. "
    linkedin_post += f"What trends are you most excited about?\n\n"
    linkedin_post += f"#AI #Technology #Innovation #TechTrends #ArtificialIntelligence #DigitalTransformation #Innovation"
    
    return {
        "x": x_post,
        "instagram": instagram_post,
        "linkedin": linkedin_post
    }

def publish_daily_post(title, content, category_name="Daily Roundup"):
    """Publish the daily post to WordPress"""
    print(f"📤 Publishing daily post: {title}")
    
    auth_header = create_auth_header()
    if not auth_header:
        print("❌ WordPress credentials not available")
        return False
    
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Get or create category
        category_id = get_or_create_category(category_name)
        
        post_data = {
            'title': title,
            'content': content,
            'status': 'publish',
            'categories': [category_id],
        }
        
        headers = {
            'Authorization': auth_header,
            'Content-Type': 'application/json'
        }
        
        # Post to WordPress
        api_url = f"{WP_URL}/wp-json/wp/v2/posts"
        
        response = requests.post(
            api_url, 
            headers=headers, 
            data=json.dumps(post_data), verify=False, timeout=60
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 201:
            post_data = response.json()
            post_id = post_data.get('id')
            post_url = post_data.get('link')
            print(f"✅ Daily post published successfully!")
            print(f"   Post ID: {post_id}")
            print(f"   URL: {post_url}")
            return True
        else:
            print(f"❌ Failed to publish post")
            print(f"Response: {response.text[:300]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error publishing to WordPress: {e}")
        return False

def save_social_posts_to_file(posts, filename="social_media_posts.txt"):
    """Save social media posts to a file for easy copying"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("SOCIAL MEDIA POSTS FOR TODAY\n")
            f.write("=" * 60 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("🐦 X (Twitter) Post:\n")
            f.write("-" * 30 + "\n")
            f.write(posts['x'] + "\n\n")
            
            f.write("📸 Instagram Post:\n")
            f.write("-" * 30 + "\n")
            f.write(posts['instagram'] + "\n\n")
            
            f.write("💼 LinkedIn Post:\n")
            f.write("-" * 30 + "\n")
            f.write(posts['linkedin'] + "\n\n")
            
            f.write("=" * 60 + "\n")
            f.write("Copy and paste these posts to your social media platforms\n")
            f.write("=" * 60 + "\n")
        
        print(f"✅ Social media posts saved to {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving social posts: {e}")
        return False

def main():
    """Main daily content generation workflow"""
    print("🚀 MyTribal.AI Daily Content & Social Media Generator")
    print("=" * 70)
    print("📅 Morning Edition - Generating daily content and social posts")
    print("=" * 70)
    
    # Check WordPress connection
    auth_header = create_auth_header()
    if not auth_header:
        print("❌ Cannot proceed without WordPress credentials")
        return
    
    # Step 1: Fetch trending topics
    topics = fetch_trending_topics()
    if not topics:
        print("❌ No trending topics found")
        return
    
    print(f"\n📊 Top trending topics for today:")
    for i, topic in enumerate(topics[:3], 1):
        print(f"   {i}. {topic['title'][:60]}...")
    
    # Step 2: Generate daily article
    print(f"\n✍️ Generating daily article...")
    article = generate_daily_article(topics)
    if not article:
        print("❌ Failed to generate article")
        return
    
    # Step 3: Generate social media posts
    print(f"\n📱 Generating social media posts...")
    social_posts = generate_social_media_posts(article, topics)
    if not social_posts:
        print("❌ Failed to generate social posts")
        return
    
    # Step 4: Publish daily post to WordPress
    title = f"Today's AI & Tech Roundup - {datetime.now().strftime('%B %d, %Y')}"
    if publish_daily_post(title, article):
        print(f"✅ Daily post published to MyTribal.AI")
    else:
        print(f"⚠️ Daily post publishing failed")
    
    # Step 5: Save social media posts
    save_social_posts_to_file(social_posts)
    
    print(f"\n🎉 Daily Content Generation Complete!")
    print(f"=" * 70)
    print(f"📝 Daily post: {title}")
    print(f"📱 Social posts saved to: social_media_posts.txt")
    print(f"🌐 Check your site: {WP_URL}")
    print(f"=" * 70)
    
    # Display social posts for easy copying
    print(f"\n📱 SOCIAL MEDIA POSTS READY TO COPY:")
    print(f"=" * 50)
    
    print(f"\n🐦 X (Twitter):")
    print(f"-" * 20)
    print(social_posts['x'])
    
    print(f"\n📸 Instagram:")
    print(f"-" * 20)
    print(social_posts['instagram'])
    
    print(f"\n💼 LinkedIn:")
    print(f"-" * 20)
    print(social_posts['linkedin'])

if __name__ == "__main__":
    main()
