#!/usr/bin/env python3
"""
Create or update a Contact page on WordPress via REST API.
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
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        resp = requests.get(url, headers=headers, verify=False, timeout=30)
        if resp.status_code == 200:
            pages = resp.json()
            return pages[0] if pages else None
        else:
            print(f"⚠️ Unexpected response when searching page: {resp.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error fetching page by slug: {e}")
        return None


def build_contact_content() -> str:
    """Return HTML content for the Contact page."""
    year = datetime.now().year
    return f"""
<div class="contact-page" style="max-width: 900px; margin: 0 auto; padding: 20px; color: #000000; line-height: 1.6;">
  <h1 style="color: #000000;">Contact Us</h1>
  
  <p style="color: #000000; font-size: 1.1em;">Have a project in mind? Let's discuss how we can help you achieve your goals.</p>

  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 32px; margin: 40px 0;">
    
    <div style="background: #f9fafb; padding: 24px; border-radius: 12px;">
      <h2 style="color: #000000; margin-top: 0;">Email</h2>
      <p style="color: #000000;">For inquiries, project discussions, or general questions:</p>
      <p style="color: #000000;">
        <a href="mailto:admin@mytribal.ai" style="color: #2563eb; font-size: 1.1em; font-weight: 600;">admin@mytribal.ai</a>
      </p>
      <p style="color: #666666; font-size: 0.9em; margin-top: 16px;">We typically respond within 24-48 hours.</p>
    </div>

    <div style="background: #f9fafb; padding: 24px; border-radius: 12px;">
      <h2 style="color: #000000; margin-top: 0;">Book a Consultation</h2>
      <p style="color: #000000;">Schedule a free 20-minute consultation to discuss your project:</p>
      <p style="margin-top: 16px;">
        <a href="{BOOKING_URL}" target="_blank" rel="noopener" style="display: inline-block; background: #2563eb; color: #fff; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600;">Book Now</a>
      </p>
      <p style="color: #666666; font-size: 0.9em; margin-top: 16px;">Choose a time that works for you.</p>
    </div>

  </div>

  <h2 style="color: #000000; margin-top: 48px;">What to Include in Your Inquiry</h2>
  <p style="color: #000000;">To help us provide the best response, please include:</p>
  <ul style="color: #000000;">
    <li><strong>Project Overview:</strong> Brief description of what you need</li>
    <li><strong>Timeline:</strong> When you need the work completed</li>
    <li><strong>Budget Range:</strong> Rough estimate (if applicable)</li>
    <li><strong>Current Challenges:</strong> What problems are you trying to solve?</li>
  </ul>

  <h2 style="color: #000000; margin-top: 48px;">Service Areas</h2>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 24px 0;">
    <div style="padding: 20px; border: 1px solid #e5e7eb; border-radius: 8px;">
      <h3 style="color: #000000; margin-top: 0;">Website Fix</h3>
      <p style="color: #000000; font-size: 0.9em;">Performance optimization, bug fixes, plugin conflicts, SEO improvements</p>
    </div>
    <div style="padding: 20px; border: 1px solid #e5e7eb; border-radius: 8px;">
      <h3 style="color: #000000; margin-top: 0;">AI Automations</h3>
      <p style="color: #000000; font-size: 0.9em;">Content pipelines, lead triage, data syncs, workflow automation</p>
    </div>
    <div style="padding: 20px; border: 1px solid #e5e7eb; border-radius: 8px;">
      <h3 style="color: #000000; margin-top: 0;">AI/ML Consulting</h3>
      <p style="color: #000000; font-size: 0.9em;">Problem framing, model development, RAG systems, MLOps</p>
    </div>
  </div>

  <div style="background: #eff6ff; border-left: 4px solid #2563eb; padding: 20px; border-radius: 8px; margin: 40px 0;">
    <h3 style="color: #000000; margin-top: 0;">Quick Links</h3>
    <p style="color: #000000; margin-bottom: 12px;">
      <a href="/services/" style="color: #2563eb; text-decoration: underline;">View All Services →</a>
    </p>
    <p style="color: #000000; margin-bottom: 12px;">
      <a href="/case-studies/" style="color: #2563eb; text-decoration: underline;">See Case Studies →</a>
    </p>
    <p style="color: #000000; margin-bottom: 0;">
      <a href="/about/" style="color: #2563eb; text-decoration: underline;">Learn More About Us →</a>
    </p>
  </div>

  <h2 style="color: #000000; margin-top: 48px;">Other Information</h2>
  <p style="color: #000000;">
    <strong>Website:</strong> <a href="https://mytribal.ai" style="color: #2563eb;">https://mytribal.ai</a><br>
    <strong>Response Time:</strong> We aim to respond to all inquiries within 24-48 hours during business days.<br>
    <strong>Location:</strong> Serving clients worldwide remotely
  </p>

  <p style="margin-top: 48px; color: #666666; font-size: 0.9em;">© {year} MyTribal AI. All rights reserved.</p>
</div>
""".strip()


def create_or_update_contact_page():
    auth = create_auth_header()
    if not auth:
        print("❌ Missing WP credentials. Set WP_USERNAME and WP_APP_PASSWORD in your environment.")
        return False

    headers = {
        'Authorization': auth,
        'Content-Type': 'application/json',
    }

    content_html = build_contact_content()
    title = "Contact"
    slug = "contact"

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
                print(f"✅ Updated Contact page (ID: {page_id})")
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
                print(f"✅ Created Contact page (ID: {data.get('id')})")
                return True
            else:
                print(f"❌ Failed to create page: {resp.status_code}")
                print(resp.text[:300])
                return False
    except Exception as e:
        print(f"❌ Error creating/updating Contact page: {e}")
        return False


def main():
    print("🚀 Creating/Updating Contact page on WordPress...")
    ok = create_or_update_contact_page()
    if ok:
        print(f"🌐 Visit: {WP_URL}/contact/")
    else:
        print("⚠️ Operation not completed.")


if __name__ == "__main__":
    main()


