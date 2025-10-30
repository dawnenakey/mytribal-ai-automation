#!/usr/bin/env python3
"""
Create or update a Services page on WordPress via REST API.

This script will:
- Authenticate using Basic Auth (username + application password)
- Check for an existing page with slug "services"
- Create or update the page with structured content describing offerings
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
        # Suppress insecure request warnings (self-signed/disabled verification)
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


def build_services_content() -> str:
    """Return HTML content for the Services page."""
    year = datetime.now().year
    # Inline JSON-LD for FAQ schema
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "How quickly can you start?",
                "acceptedAnswer": {"@type": "Answer", "text": "Discovery within 1–2 business days. Fixes often same week; consulting starts within a week."}
            },
            {
                "@type": "Question",
                "name": "Do you offer fixed quotes?",
                "acceptedAnswer": {"@type": "Answer", "text": "Yes for Website Fix work. Consulting is milestone-based with clear deliverables."}
            },
            {
                "@type": "Question",
                "name": "Who owns the IP?",
                "acceptedAnswer": {"@type": "Answer", "text": "You own the deliverables and code produced for your project."}
            },
            {
                "@type": "Question",
                "name": "What stacks do you support?",
                "acceptedAnswer": {"@type": "Answer", "text": "WordPress, Python, OpenAI/LLMs, Notion, and common cloud tooling (plus integrations)."}
            }
        ]
    }

    return f"""
<div class="services-page">
  <style>
    /* Sticky CTA */
    .sticky-cta {{
      position: sticky; bottom: 0; background: #0f172a; color: #fff; padding: 12px 16px;
      display: flex; justify-content: space-between; align-items: center; gap: 12px; z-index: 50;
    }}
    .sticky-cta a {{ background: #22c55e; color: #0b1220; padding: 10px 16px; border-radius: 8px; text-decoration: none; font-weight: 600; }}
    .packages {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin: 12px 0 24px; }}
    .package {{ border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; }}
    .package h3 {{ margin-top: 0; }}
    .package ul {{ padding-left: 18px; }}
    .services-page .cta-btn {{ display: inline-block; background: #2563eb; color: #fff; padding: 10px 16px; border-radius: 8px; text-decoration: none; font-weight: 600; }}
  </style>

  <div class="sticky-cta">
    <span>Ready to move fast with confidence?</span>
    <a href="{BOOKING_URL}" target="_blank" rel="noopener" class="cta-btn" data-ga4="book_consult">Book a consultation</a>
  </div>

  <h1>Professional Services</h1>
  <p>We help founders and teams ship faster with pragmatic fixes and automation that actually works.</p>
  <p><a href="/case-studies/" style="color: #2563eb; text-decoration: underline;">📊 View case studies and results →</a></p>

  <hr/>

  <h2>Website Fix</h2>
  <p>Stuck with a broken page, slow load times, or plugin conflicts? We provide rapid diagnosis and fixes for WordPress and modern web stacks.</p>
  <ul>
    <li>Performance tuning (Core Web Vitals, caching, CDNs)</li>
    <li>Theme and plugin conflicts, update strategy</li>
    <li>Accessibility and SEO hygiene</li>
    <li>Secure hardening and backups</li>
  </ul>

  <h3>How it works</h3>
  <ol>
    <li>Share the issue and site details</li>
    <li>We assess and give you a clear, fixed quote</li>
    <li>We implement, verify, and document the fix</li>
  </ol>

  <hr/>

  <h2>AI Automations for Your Website</h2>
  <p>Save hours weekly with AI-driven workflows integrated into your stack.</p>
  <ul>
    <li>Content workflows (RSS ➜ AI summarization ➜ scheduled publish)</li>
    <li>Lead intake triage and enrichment</li>
    <li>Support deflection and knowledge search</li>
    <li>Data syncs across CMS/CRMs and Notion</li>
  </ul>

  <h3>Tech we use</h3>
  <p>WordPress REST, OpenAI API, Python, webhooks, Notion, and modern cloud tooling.</p>

  <hr/>

  <h2>Packages</h2>
  <div class="packages">
    <div class="package">
      <h3>Starter Fix</h3>
      <p><strong>From $500</strong> • 2–3 days</p>
      <ul>
        <li>Single-issue diagnosis and resolution</li>
        <li>Performance or SEO/accessibility quick wins</li>
        <li>Before/after report</li>
      </ul>
      <a href="{BOOKING_URL}" target="_blank" rel="noopener" class="cta-btn" data-ga4="starter_fix_cta">Book consult</a>
    </div>
    <div class="package">
      <h3>Automation Pro</h3>
      <p><strong>From $2,000</strong> • 1–2 weeks</p>
      <ul>
        <li>Content pipeline (RSS → AI → scheduled publish)</li>
        <li>Lead triage and data enrichment</li>
        <li>Documentation and handover</li>
      </ul>
      <a href="{BOOKING_URL}" target="_blank" rel="noopener" class="cta-btn" data-ga4="automation_pro_cta">Book consult</a>
    </div>
    <div class="package">
      <h3>Consulting Sprint</h3>
      <p><strong>From $4,000</strong> • 2–4 weeks</p>
      <ul>
        <li>Problem framing, data strategy, baselines</li>
        <li>LLM/RAG prototype or MLOps hardening</li>
        <li>Stakeholder workshop + roadmap</li>
      </ul>
      <a href="{BOOKING_URL}" target="_blank" rel="noopener" class="cta-btn" data-ga4="consulting_sprint_cta">Book consult</a>
    </div>
  </div>

  <h2>AI/ML Consulting</h2>
  <p>From a data scientist’s perspective, I help you scope, design, and implement ML systems that deliver measurable outcomes, not just demos.</p>
  <ul>
    <li>Problem framing and feasibility assessments</li>
    <li>Data strategy, labeling plans, and evaluation design</li>
    <li>Model selection, experimentation, and baselines</li>
    <li>LLM integrations, retrieval-augmented generation (RAG), and prompt engineering</li>
    <li>MLOps: deployment, monitoring, drift detection, and lifecycle management</li>
  </ul>
  <p><strong>Credentials:</strong> MS in Data Science (University of Denver) with industry experience building reliable AI features end-to-end.</p>

  <hr/>

  <h2>FAQs</h2>
  <details><summary>How quickly can you start?</summary><div>Discovery within 1–2 business days. Fixes often same week; consulting starts within a week.</div></details>
  <details><summary>Do you offer fixed quotes?</summary><div>Yes for Website Fix work. Consulting is milestone-based with clear deliverables.</div></details>
  <details><summary>Who owns the IP?</summary><div>You own the deliverables and code produced for your project.</div></details>
  <details><summary>What stacks do you support?</summary><div>WordPress, Python, OpenAI/LLMs, Notion, and common cloud tooling (plus integrations).</div></details>

  <h2>Book a Consultation</h2>
  <p>Schedule a consultation to discuss your project needs. We'll propose a lean, maintainable solution tailored to your timeline and goals.</p>
  <p><a href="/case-studies/" style="color: #2563eb; text-decoration: underline;">See real results from past projects →</a></p>
  
  <div style="margin: 24px 0; padding: 24px; background: #f9fafb; border-radius: 12px;">
    <h3 style="margin-top: 0;">Book Your Session</h3>
    <p>Use the booking widget below to select a date and time that works for you:</p>
    <div style="margin: 20px 0;">
      <!-- SimplyBook.me Booking Widget Embed -->
      <iframe src="{BOOKING_URL}" width="100%" height="800" frameborder="0" style="border-radius: 8px; min-height: 600px;"></iframe>
    </div>
    <p style="margin-top: 12px;">
      <strong>Prefer email?</strong> <a href="mailto:admin@mytribal.ai" style="color: #2563eb;">admin@mytribal.ai</a>
      &nbsp;|&nbsp;
      <a href="{BOOKING_URL}" target="_blank" rel="noopener" class="cta-btn" data-ga4="book_consult_footer">Open booking in new tab</a>
    </p>
  </div>

  <script type="application/ld+json">{json.dumps(faq_schema)}</script>

  <script>
  // GA4 click event tracking for CTAs (requires gtag or dataLayer already on site)
  (function() {{
    function sendEvent(action) {{
      try {{
        if (window.gtag) {{ gtag('event', action, {{ 'event_category': 'services_page' }}); return; }}
        if (window.dataLayer && Array.isArray(window.dataLayer)) {{ window.dataLayer.push({{ 'event': action, 'event_category': 'services_page' }}); }}
      }} catch (e) {{ /* no-op */ }}
    }}
    document.addEventListener('click', function(e) {{
      var el = e.target.closest('[data-ga4]');
      if (!el) return;
      sendEvent(el.getAttribute('data-ga4'));
    }});
  }})();
  </script>

  <p style="margin-top: 32px; color: #666;">© {year} MyTribal AI</p>
</div>
""".strip()


def create_or_update_services_page():
    auth = create_auth_header()
    if not auth:
        print("❌ Missing WP credentials. Set WP_USERNAME and WP_APP_PASSWORD in your environment.")
        return False

    headers = {
        'Authorization': auth,
        'Content-Type': 'application/json',
    }

    content_html = build_services_content()
    title = "Services"
    slug = "services"

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
            # Suppress insecure request warnings
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            resp = requests.post(url, headers=headers, data=json.dumps(payload), verify=False, timeout=60)
            if resp.status_code == 200:
                print(f"✅ Updated Services page (ID: {page_id})")
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
            # Suppress insecure request warnings
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            resp = requests.post(url, headers=headers, data=json.dumps(payload), verify=False, timeout=60)
            if resp.status_code == 201:
                data = resp.json()
                print(f"✅ Created Services page (ID: {data.get('id')})")
                return True
            else:
                print(f"❌ Failed to create page: {resp.status_code}")
                print(resp.text[:300])
                return False
    except Exception as e:
        print(f"❌ Error creating/updating Services page: {e}")
        return False


def main():
    print("🚀 Creating/Updating Services page on WordPress...")
    ok = create_or_update_services_page()
    if ok:
        print(f"🌐 Visit: {WP_URL}/services/")
    else:
        print("⚠️ Operation not completed.")


if __name__ == "__main__":
    main()


