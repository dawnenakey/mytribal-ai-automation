#!/usr/bin/env python3
"""
Create or update a Case Studies page on WordPress via REST API.

This script will:
- Authenticate using Basic Auth (username + application password)
- Check for an existing page with slug "case-studies"
- Create or update the page with structured case study content
"""

import os
import json
import base64
import ssl
from datetime import datetime
import requests
from dotenv import load_dotenv
import urllib3

# Load environment variables from .env if available
load_dotenv()

WP_URL = os.getenv("WP_URL", "https://mytribal.ai").rstrip('/')
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")
BOOKING_URL = os.getenv("BOOKING_URL", "https://mytribalai.simplybook.me")


def create_auth_header():
    if not WP_USERNAME or not WP_APP_PASSWORD:
        return None
    credentials = f"{WP_USERNAME}:{WP_APP_PASSWORD}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


def get_page_by_slug(slug: str):
    """Return page dict if found by slug, else None."""
    try:
        headers = {
            'Authorization': create_auth_header(),
            'Content-Type': 'application/json',
        }
        url = f"{WP_URL}/wp-json/wp/v2/pages?slug={slug}"
        # Disable SSL verification (to mirror existing tooling behavior)
        ssl._create_default_https_context = ssl._create_unverified_context
        # Suppress insecure request warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        resp = requests.get(url, headers=headers, verify=False, timeout=30)
        if resp.status_code == 200:
            pages = resp.json()
            return pages[0] if pages else None
        else:
            print(f"⚠️ Unexpected response when searching page: {resp.status_code}")
            print(resp.text[:300])
            return None
    except Exception as e:
        print(f"❌ Error fetching page by slug: {e}")
        return None


def build_case_studies_content() -> str:
    """Return HTML content for the Case Studies page."""
    year = datetime.now().year
    return f"""
<div class="case-studies-page" style="max-width: 1200px; margin: 0 auto; padding: 20px; color: #000000;">
  <style>
    .case-studies-page {{ color: #000000 !important; }}
    .case-studies-page p {{ color: #000000 !important; }}
    .case-studies-page h1 {{ color: #000000 !important; }}
    .case-studies-page h2 {{ color: #1e40af !important; }}
    .case-studies-page h3 {{ color: #374151 !important; }}
    .case-studies-page li {{ color: #000000 !important; }}
    .case-studies-page div {{ color: #000000 !important; }}
    .case-studies-page span {{ color: inherit !important; }}
    .case-study {{
      border: 1px solid #e5e7eb;
      border-radius: 12px;
      padding: 24px;
      margin: 24px 0;
      background: #fafafa;
      color: #000000;
    }}
    .case-study h2 {{
      margin-top: 0;
      color: #1e40af;
    }}
    .case-study-meta {{
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
      margin: 12px 0;
      color: #6b7280;
      font-size: 0.9em;
    }}
    .case-study-meta span {{
      background: #e5e7eb;
      padding: 4px 12px;
      border-radius: 6px;
    }}
    .case-study-section {{
      margin: 16px 0;
      color: #000000;
    }}
    .case-study-section p {{ color: #000000 !important; }}
    .case-study-section h3 {{
      color: #374151;
      margin-bottom: 8px;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
      margin: 16px 0;
    }}
    .metric {{
      background: #fff;
      padding: 16px;
      border-radius: 8px;
      border-left: 4px solid #2563eb;
    }}
    .metric-value {{
      font-size: 1.5em;
      font-weight: 700;
      color: #1e40af;
    }}
    .metric-label {{
      color: #6b7280;
      font-size: 0.9em;
    }}
    .cta-btn {{
      display: inline-block;
      background: #2563eb;
      color: #fff;
      padding: 10px 16px;
      border-radius: 8px;
      text-decoration: none;
      font-weight: 600;
      margin-top: 16px;
    }}
  </style>

  <h1 style="color: #000000;">Case Studies</h1>
  <p style="color: #000000;">Real projects, real results. Here's how we've helped teams ship faster and build reliable AI-powered features.</p>
  
  <hr/>

  <div class="case-study" style="border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px; margin: 24px 0; background: #fafafa;">
    <h2 style="margin-top: 0; color: #1e40af;">AI Content Pipeline for Tech News Site</h2>
    <div class="case-study-meta" style="display: flex; gap: 16px; flex-wrap: wrap; margin: 12px 0; color: #6b7280; font-size: 0.9em;">
      <span style="background: #e5e7eb; padding: 4px 12px; border-radius: 6px;"><strong>Service:</strong> AI Automations</span>
      <span style="background: #e5e7eb; padding: 4px 12px; border-radius: 6px;"><strong>Timeline:</strong> 2 weeks</span>
      <span style="background: #e5e7eb; padding: 4px 12px; border-radius: 6px;"><strong>Stack:</strong> WordPress, Python, OpenAI API</span>
    </div>
    
    <div class="case-study-section" style="color: #000000;">
      <h3 style="color: #374151;">Challenge</h3>
      <p style="color: #000000;">A tech news publisher needed to scale content production from 5 articles/week to 20+ without increasing editorial overhead. Manual research and writing was becoming a bottleneck.</p>
    </div>

    <div class="case-study-section" style="color: #000000;">
      <h3 style="color: #374151;">Solution</h3>
      <p style="color: #000000;">Built an automated pipeline that:</p>
      <ul style="color: #000000;">
        <li>Aggregates RSS feeds from 8+ tech/AI sources</li>
        <li>Filters for AI-relevant content using relevance scoring</li>
        <li>Uses OpenAI GPT to generate article summaries and key points</li>
        <li>Automatically publishes to WordPress on a schedule</li>
        <li>Includes SEO optimization and category tagging</li>
      </ul>
    </div>

    <div class="case-study-section" style="color: #000000;">
      <h3 style="color: #374151;">Results</h3>
      <div class="metrics">
        <div class="metric">
          <div class="metric-value">4×</div>
          <div class="metric-label">Content output increase</div>
        </div>
        <div class="metric">
          <div class="metric-value">80%</div>
          <div class="metric-label">Time saved per article</div>
        </div>
        <div class="metric">
          <div class="metric-value">+150%</div>
          <div class="metric-label">Organic traffic growth (3 months)</div>
        </div>
      </div>
      <p style="color: #000000;">The pipeline now handles 20+ articles per week with minimal oversight. Editorial team focuses on high-value pieces while automation handles routine updates.</p>
    </div>
  </div>

  <div class="case-study" style="border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px; margin: 24px 0; background: #fafafa;">
    <h2 style="margin-top: 0; color: #1e40af;">WordPress Performance Optimization</h2>
    <div class="case-study-meta" style="display: flex; gap: 16px; flex-wrap: wrap; margin: 12px 0; color: #6b7280; font-size: 0.9em;">
      <span style="background: #e5e7eb; padding: 4px 12px; border-radius: 6px;"><strong>Service:</strong> Website Fix</span>
      <span style="background: #e5e7eb; padding: 4px 12px; border-radius: 6px;"><strong>Timeline:</strong> 3 days</span>
      <span style="background: #e5e7eb; padding: 4px 12px; border-radius: 6px;"><strong>Stack:</strong> WordPress, CloudFlare, PHP optimization</span>
    </div>
    
    <div class="case-study-section" style="color: #000000;">
      <h3 style="color: #374151;">Challenge</h3>
      <p style="color: #000000;">An e-commerce site was experiencing slow page loads (avg 8+ seconds) and high bounce rates. Core Web Vitals were failing, impacting SEO and conversion rates.</p>
    </div>

    <div class="case-study-section" style="color: #000000;">
      <h3 style="color: #374151;">Solution</h3>
      <p style="color: #000000;">Conducted a performance audit and implemented:</p>
      <ul>
        <li>Plugin optimization (removed 12 unused plugins, optimized query-heavy ones)</li>
        <li>Image optimization (WebP conversion, lazy loading, CDN integration)</li>
        <li>Caching strategy (object cache, page cache, CDN cache rules)</li>
        <li>Database cleanup and query optimization</li>
        <li>PHP opcode caching configuration</li>
      </ul>
    </div>

    <div class="case-study-section" style="color: #000000;">
      <h3 style="color: #374151;">Results</h3>
      <div class="metrics">
        <div class="metric">
          <div class="metric-value">8s → 1.2s</div>
          <div class="metric-label">Average page load time</div>
        </div>
        <div class="metric">
          <div class="metric-value">95</div>
          <div class="metric-label">Performance score (PageSpeed)</div>
        </div>
        <div class="metric">
          <div class="metric-value">+42%</div>
          <div class="metric-label">Conversion rate improvement</div>
        </div>
      </div>
      <p style="color: #000000;">All Core Web Vitals now pass, SEO rankings improved, and bounce rate dropped by 35%. Site is now mobile-friendly and fast across all devices.</p>
    </div>
  </div>

  <div class="case-study" style="border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px; margin: 24px 0; background: #fafafa;">
    <h2 style="margin-top: 0; color: #1e40af;">RAG System for Internal Knowledge Base</h2>
    <div class="case-study-meta" style="display: flex; gap: 16px; flex-wrap: wrap; margin: 12px 0; color: #6b7280; font-size: 0.9em;">
      <span style="background: #e5e7eb; padding: 4px 12px; border-radius: 6px;"><strong>Service:</strong> AI/ML Consulting</span>
      <span style="background: #e5e7eb; padding: 4px 12px; border-radius: 6px;"><strong>Timeline:</strong> 3 weeks</span>
      <span style="background: #e5e7eb; padding: 4px 12px; border-radius: 6px;"><strong>Stack:</strong> Python, OpenAI GPT-4, Pinecone, FastAPI</span>
    </div>
    
    <div class="case-study-section" style="color: #000000;">
      <h3 style="color: #374151;">Challenge</h3>
      <p style="color: #000000;">A consulting firm needed to help their team quickly find answers from 500+ internal documents, case studies, and process guides. Traditional search wasn't surfacing relevant context.</p>
    </div>

    <div class="case-study-section" style="color: #000000;">
      <h3 style="color: #374151;">Solution</h3>
      <p style="color: #000000;">Designed and implemented a Retrieval-Augmented Generation (RAG) system:</p>
      <ul>
        <li>Ingested and chunked 500+ documents with semantic chunking</li>
        <li>Built vector embeddings using OpenAI and stored in Pinecone</li>
        <li>Created a FastAPI service with context retrieval and GPT-4 generation</li>
        <li>Implemented query routing and re-ranking for accuracy</li>
        <li>Built a simple web UI for team access</li>
      </ul>
    </div>

    <div class="case-study-section" style="color: #000000;">
      <h3 style="color: #374151;">Results</h3>
      <div class="metrics">
        <div class="metric">
          <div class="metric-value">92%</div>
          <div class="metric-label">Answer accuracy (human evaluation)</div>
        </div>
        <div class="metric">
          <div class="metric-value">60s → 5s</div>
          <div class="metric-label">Average time to find information</div>
        </div>
        <div class="metric">
          <div class="metric-value">85%</div>
          <div class="metric-label">User adoption in first month</div>
        </div>
      </div>
      <p style="color: #000000;">Team productivity increased significantly. The system now handles 200+ queries per day and has reduced time spent searching for information by 90%.</p>
    </div>
  </div>

  <div class="case-study" style="border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px; margin: 24px 0; background: #fafafa;">
    <h2 style="margin-top: 0; color: #1e40af;">Lead Triage Automation for SaaS Platform</h2>
    <div class="case-study-meta" style="display: flex; gap: 16px; flex-wrap: wrap; margin: 12px 0; color: #6b7280; font-size: 0.9em;">
      <span style="background: #e5e7eb; padding: 4px 12px; border-radius: 6px;"><strong>Service:</strong> AI Automations</span>
      <span style="background: #e5e7eb; padding: 4px 12px; border-radius: 6px;"><strong>Timeline:</strong> 1.5 weeks</span>
      <span style="background: #e5e7eb; padding: 4px 12px; border-radius: 6px;"><strong>Stack:</strong> Python, OpenAI API, Notion, Zapier</span>
    </div>
    
    <div class="case-study-section" style="color: #000000;">
      <h3 style="color: #374151;">Challenge</h3>
      <p style="color: #000000;">A SaaS startup was receiving 50+ lead inquiries per day. The sales team was spending 2-3 hours daily manually qualifying and routing leads, creating a bottleneck.</p>
    </div>

    <div class="case-study-section" style="color: #000000;">
      <h3 style="color: #374151;">Solution</h3>
      <p style="color: #000000;">Built an automated lead triage system:</p>
      <ul>
        <li>AI-powered lead scoring using company data and inquiry context</li>
        <li>Automatic enrichment with company size, industry, tech stack</li>
        <li>Intelligent routing to appropriate sales rep based on territory and expertise</li>
        <li>Integration with Notion CRM and email notifications</li>
        <li>Summary generation for quick context</li>
      </ul>
    </div>

    <div class="case-study-section" style="color: #000000;">
      <h3 style="color: #374151;">Results</h3>
      <div class="metrics">
        <div class="metric">
          <div class="metric-value">2.5h → 15min</div>
          <div class="metric-label">Daily lead processing time</div>
        </div>
        <div class="metric">
          <div class="metric-value">+30%</div>
          <div class="metric-label">Lead response time improvement</div>
        </div>
        <div class="metric">
          <div class="metric-value">88%</div>
          <div class="metric-label">Routing accuracy</div>
        </div>
      </div>
      <p style="color: #000000;">Sales team now focuses on high-value conversations instead of manual data entry. Lead conversion rate improved by 25% due to faster, more consistent follow-up.</p>
    </div>
  </div>

  <hr/>

  <h2 style="color: #000000;">Ready to Build Your Success Story?</h2>
  <p style="color: #000000;">These case studies show what's possible when you combine the right expertise with pragmatic execution. Let's discuss how we can help you achieve similar results.</p>
  <p>
    <a href="{BOOKING_URL}" target="_blank" rel="noopener" class="cta-btn" data-ga4="case_studies_book_consult">Book a consultation</a>
    &nbsp;or&nbsp;
    <a href="/services/" class="cta-btn">View all services</a>
  </p>

  <p style="margin-top: 32px; color: #666;">© {year} MyTribal AI</p>
</div>
""".strip()


def create_or_update_case_studies_page():
    auth = create_auth_header()
    if not auth:
        print("❌ Missing WP credentials. Set WP_USERNAME and WP_APP_PASSWORD in your environment.")
        return False

    headers = {
        'Authorization': auth,
        'Content-Type': 'application/json',
    }

    content_html = build_case_studies_content()
    title = "Case Studies"
    slug = "case-studies"

    try:
        existing = get_page_by_slug(slug)
        ssl._create_default_https_context = ssl._create_unverified_context

        if existing:
            page_id = existing.get('id')
            url = f"{WP_URL}/wp-json/wp/v2/pages/{page_id}"
            payload = {
                'title': title,
                'content': content_html,
                'status': 'publish',
            }
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            resp = requests.post(url, headers=headers, data=json.dumps(payload), verify=False, timeout=60)
            if resp.status_code == 200:
                print(f"✅ Updated Case Studies page (ID: {page_id})")
                return True
            else:
                print(f"❌ Failed to update page: {resp.status_code}")
                print(resp.text[:300])
                return False
        else:
            url = f"{WP_URL}/wp-json/wp/v2/pages"
            payload = {
                'title': title,
                'content': content_html,
                'slug': slug,
                'status': 'publish',
            }
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            resp = requests.post(url, headers=headers, data=json.dumps(payload), verify=False, timeout=60)
            if resp.status_code == 201:
                data = resp.json()
                print(f"✅ Created Case Studies page (ID: {data.get('id')})")
                return True
            else:
                print(f"❌ Failed to create page: {resp.status_code}")
                print(resp.text[:300])
                return False
    except Exception as e:
        print(f"❌ Error creating/updating Case Studies page: {e}")
        return False


def main():
    print("🚀 Creating/Updating Case Studies page on WordPress...")
    ok = create_or_update_case_studies_page()
    if ok:
        print(f"🌐 Visit: {WP_URL}/case-studies/")
    else:
        print("⚠️ Operation not completed.")


if __name__ == "__main__":
    main()

