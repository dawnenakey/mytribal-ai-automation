#!/usr/bin/env python3
"""
Create or update an About Us page on WordPress via REST API.
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


def build_about_content() -> str:
    """Return HTML content for the About Us page."""
    year = datetime.now().year
    return f"""
<div class="about-page" style="max-width: 900px; margin: 0 auto; padding: 20px; color: #000000; line-height: 1.6;">
  <h1 style="color: #000000;">About MyTribal AI</h1>
  
  <p style="color: #000000; font-size: 1.1em;">We help founders and teams ship faster with pragmatic fixes and automation that actually works.</p>

  <h2 style="color: #000000; margin-top: 32px;">Who We Are</h2>
  <p style="color: #000000;">MyTribal AI is a technology consulting company specializing in AI/ML solutions, website optimization, and automation. We combine technical expertise with a practical, results-driven approach to help businesses leverage cutting-edge technology.</p>

  <h2 style="color: #000000; margin-top: 32px;">Our Expertise</h2>
  <p style="color: #000000;">Our team brings deep expertise in:</p>
  <ul style="color: #000000;">
    <li><strong>AI/ML Consulting:</strong> From problem framing to deployment, we help you build reliable machine learning systems that deliver measurable outcomes</li>
    <li><strong>Website Optimization:</strong> Performance tuning, SEO, accessibility, and security for WordPress and modern web stacks</li>
    <li><strong>Automation Solutions:</strong> Custom AI-powered workflows that save time and scale your operations</li>
  </ul>

  <h2 style="color: #000000; margin-top: 32px;">Our Founder</h2>
  <p style="color: #000000;">Founded by a data scientist with a Master's degree in Data Science from the University of Denver, MyTribal AI combines academic rigor with industry experience. Our approach is grounded in:</p>
  <ul style="color: #000000;">
    <li>Evidence-based problem solving</li>
    <li>Pragmatic implementation over theory</li>
    <li>Clear communication and documentation</li>
    <li>Focus on measurable business outcomes</li>
  </ul>

  <h2 style="color: #000000; margin-top: 32px;">What We Do</h2>
  <p style="color: #000000;">We provide three core services:</p>
  
  <h3 style="color: #000000; margin-top: 24px;">Website Fix</h3>
  <p style="color: #000000;">Stuck with a broken page, slow load times, or plugin conflicts? We provide rapid diagnosis and fixes for WordPress and modern web stacks. Our performance optimizations have helped sites reduce load times from 8+ seconds to under 2 seconds.</p>

  <h3 style="color: #000000; margin-top: 24px;">AI Automations</h3>
  <p style="color: #000000;">We build custom automation solutions including content pipelines, lead triage systems, and data synchronization workflows. Our AI-powered automations help teams save hours weekly while improving consistency and scalability.</p>

  <h3 style="color: #000000; margin-top: 24px;">AI/ML Consulting</h3>
  <p style="color: #000000;">From feasibility assessments to production deployment, we help you navigate the entire ML lifecycle. Whether you need help with LLM integrations, RAG systems, or MLOps infrastructure, we bring the right mix of theory and practical experience.</p>

  <h2 style="color: #000000; margin-top: 32px;">Our Approach</h2>
  <p style="color: #000000;">We believe in:</p>
  <ul style="color: #000000;">
    <li><strong>Pragmatism over perfection:</strong> We ship solutions that work today, not demos that work tomorrow</li>
    <li><strong>Transparency:</strong> Clear communication, fixed quotes where possible, and no surprises</li>
    <li><strong>Results-focused:</strong> Every project is tied to measurable business outcomes</li>
    <li><strong>Continuous improvement:</strong> We build systems that can evolve with your needs</li>
  </ul>

  <h2 style="color: #000000; margin-top: 32px;">Get Started</h2>
  <p style="color: #000000;">Ready to work together? Whether you need a quick website fix or a comprehensive AI strategy, we're here to help.</p>
  <p style="color: #000000;">
    <a href="{BOOKING_URL}" target="_blank" rel="noopener" style="display: inline-block; background: #2563eb; color: #fff; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; margin-top: 16px;">Book a Consultation</a>
    &nbsp;&nbsp;
    <a href="/services/" style="display: inline-block; background: #f3f4f6; color: #2563eb; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; margin-top: 16px;">View Our Services</a>
  </p>

  <h2 style="color: #000000; margin-top: 32px;">Contact</h2>
  <p style="color: #000000;">
    <strong>Email:</strong> <a href="mailto:admin@mytribal.ai">admin@mytribal.ai</a><br>
    <strong>Website:</strong> <a href="https://mytribal.ai">https://mytribal.ai</a>
  </p>

  <p style="margin-top: 48px; color: #666666; font-size: 0.9em;">© {year} MyTribal AI. All rights reserved.</p>
</div>
""".strip()


def create_or_update_about_page():
    auth = create_auth_header()
    if not auth:
        print("❌ Missing WP credentials. Set WP_USERNAME and WP_APP_PASSWORD in your environment.")
        return False

    headers = {
        'Authorization': auth,
        'Content-Type': 'application/json',
    }

    content_html = build_about_content()
    title = "About Us"
    slug = "about"

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
                print(f"✅ Updated About Us page (ID: {page_id})")
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
                print(f"✅ Created About Us page (ID: {data.get('id')})")
                return True
            else:
                print(f"❌ Failed to create page: {resp.status_code}")
                print(resp.text[:300])
                return False
    except Exception as e:
        print(f"❌ Error creating/updating About Us page: {e}")
        return False


def main():
    print("🚀 Creating/Updating About Us page on WordPress...")
    ok = create_or_update_about_page()
    if ok:
        print(f"🌐 Visit: {WP_URL}/about/")
    else:
        print("⚠️ Operation not completed.")


if __name__ == "__main__":
    main()


