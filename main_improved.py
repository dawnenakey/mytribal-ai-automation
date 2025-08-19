import feedparser
from openai import OpenAI
from notion_client import Client as NotionClient
from wordpress_xmlrpc import Client as WPClient
from wordpress_xmlrpc.methods.posts import NewPost
import requests
from dotenv import load_dotenv
import os
import ssl
import urllib3

# Disable SSL warnings for testing (remove in production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()  # Load variables from .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")
WP_SSL_VERIFY = os.getenv("WP_SSL_VERIFY", "true").lower() == "true"

# Alternative RSS feeds (more reliable than Reddit)
RSS_URLS = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://feeds.arstechnica.com/arstechnica/index"
]

# Initialize clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)
notion_client = NotionClient(auth=NOTION_API_KEY)

# Initialize WordPress client with SSL verification option
if WP_SSL_VERIFY:
    wp_client = WPClient(WP_URL, WP_USERNAME, WP_APP_PASSWORD)
else:
    # Create a custom session with SSL verification disabled
    import requests
    session = requests.Session()
    session.verify = False
    wp_client = WPClient(WP_URL, WP_USERNAME, WP_APP_PASSWORD, session=session)

def fetch_rss_content():
    """Fetch content from RSS feeds with fallback options"""
    for url in RSS_URLS:
        try:
            print(f"Trying RSS feed: {url}")
            
            # Add user-agent to avoid being blocked
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            
            if feed.entries and len(feed.entries) > 0:
                print(f"✅ Successfully fetched {len(feed.entries)} entries from {url}")
                return feed.entries[:3]  # Limit to 3 entries for testing
                
        except Exception as e:
            print(f"❌ Failed to fetch from {url}: {e}")
            continue
    
    print("❌ All RSS feeds failed. Using fallback content.")
    return None

def generate_article(title, description):
    """Generate article using OpenAI"""
    try:
        article_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user", 
                "content": f"Generate a 300-word blog article based on this tech news: Title: {title}. Description: {description}. Include SEO keywords like 'trending 2025', headings, and bullet points. Make it original and engaging."
            }],
            max_tokens=500
        )
        return article_response.choices[0].message.content
    except Exception as e:
        print(f"❌ Error generating article: {e}")
        return f"Article about: {title}\n\n{description}\n\nThis is a placeholder article generated due to an error in the AI service."

def generate_image(title, description):
    """Generate image using DALL-E"""
    try:
        image_response = openai_client.images.generate(
            model="dall-e-3",
            prompt=f"{title} - Create a high-quality, eye-catching image for this blog post. Include elements from: {description}. Style: vibrant digital illustration.",
            size="1024x1024",
            quality="standard",
            n=1
        )
        return image_response.data[0].url
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        return "https://via.placeholder.com/1024x1024/007bff/ffffff?text=AI+Generated+Image"

def save_to_notion(title, article, image_url):
    """Save content to Notion"""
    try:
        notion_client.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties={
                "Title": {"title": [{"text": {"content": title}}]},
                "Content": {"rich_text": [{"text": {"content": article}}]},
                "Image URL": {"url": image_url},
                "Status": {"select": {"name": "Draft"}}
            }
        )
        print(f"✅ Saved to Notion: {title}")
        return True
    except Exception as e:
        print(f"❌ Error saving to Notion: {e}")
        return False

def publish_to_wordpress(title, article, image_url):
    """Publish to WordPress"""
    try:
        post = {
            'title': title,
            'content': f"{article}\n\n<img src='{image_url}' alt='{title}' style='max-width: 100%; height: auto;'>",
            'status': 'draft'  # Changed to draft for safety during testing
        }
        wp_client.call(NewPost(post))
        print(f"✅ Published to WordPress: {title}")
        return True
    except Exception as e:
        print(f"❌ Error publishing to WordPress: {e}")
        return False

def main():
    """Main automation workflow"""
    print("🚀 Starting AI Content Automation...")
    
    # Fetch RSS content
    entries = fetch_rss_content()
    if not entries:
        print("❌ No content to process. Exiting.")
        return
    
    success_count = 0
    
    for i, entry in enumerate(entries, 1):
        print(f"\n📝 Processing entry {i}/{len(entries)}")
        print(f"Title: {entry.title}")
        
        title = entry.title
        description = entry.get("contentSnippet", entry.get("summary", "Tech news"))
        
        # Generate article
        print("🤖 Generating article...")
        article = generate_article(title, description)
        
        # Generate image
        print("🎨 Generating image...")
        image_url = generate_image(title, description)
        
        # Save to Notion
        print("📚 Saving to Notion...")
        notion_success = save_to_notion(title, article, image_url)
        
        # Publish to WordPress
        print("🌐 Publishing to WordPress...")
        wp_success = publish_to_wordpress(title, article, image_url)
        
        if notion_success and wp_success:
            success_count += 1
            print(f"✅ Entry {i} completed successfully!")
        else:
            print(f"⚠️ Entry {i} had some issues")
        
        print("-" * 50)
    
    print(f"\n🎉 Automation completed! {success_count}/{len(entries)} entries processed successfully.")
    print("Check Notion and WordPress for the generated content.")

if __name__ == "__main__":
    main()

