#!/usr/bin/env python3
"""
Create or update a Privacy Policy page on WordPress via REST API.
Required for Google AdSense approval.
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


def build_privacy_policy_content() -> str:
    """Return HTML content for the Privacy Policy page."""
    year = datetime.now().year
    return f"""
<div class="privacy-policy-page" style="max-width: 900px; margin: 0 auto; padding: 20px; color: #000000; line-height: 1.6;">
  <h1 style="color: #000000;">Privacy Policy</h1>
  <p style="color: #666666; font-size: 0.9em;">Last updated: {datetime.now().strftime('%B %d, %Y')}</p>
  
  <p style="color: #000000;">At mytribal.ai, we respect your privacy and are committed to protecting your personal data. This privacy policy explains how we collect, use, and safeguard your information when you visit our website.</p>

  <h2 style="color: #000000; margin-top: 32px;">Information We Collect</h2>
  <p style="color: #000000;">We may collect the following types of information:</p>
  <ul style="color: #000000;">
    <li><strong>Personal Information:</strong> When you contact us or subscribe to our newsletter, we may collect your name and email address.</li>
    <li><strong>Usage Data:</strong> We automatically collect information about how you interact with our website, including IP address, browser type, pages visited, and time spent on pages.</li>
    <li><strong>Cookies:</strong> We use cookies and similar tracking technologies to enhance your browsing experience and analyze site traffic.</li>
  </ul>

  <h2 style="color: #000000; margin-top: 32px;">How We Use Your Information</h2>
  <p style="color: #000000;">We use the information we collect to:</p>
  <ul style="color: #000000;">
    <li>Provide and improve our services</li>
    <li>Respond to your inquiries and provide customer support</li>
    <li>Send you newsletters and updates (with your consent)</li>
    <li>Analyze website usage and trends</li>
    <li>Ensure website security and prevent fraud</li>
  </ul>

  <h2 style="color: #000000; margin-top: 32px;">Third-Party Services</h2>
  <p style="color: #000000;">Our website uses third-party services that may collect information about you:</p>
  
  <h3 style="color: #000000; margin-top: 24px;">Google AdSense</h3>
  <p style="color: #000000;">We use Google AdSense to display advertisements on our website. Google AdSense uses cookies and other tracking technologies to:</p>
  <ul style="color: #000000;">
    <li>Serve personalized ads based on your browsing behavior</li>
    <li>Measure ad performance and effectiveness</li>
    <li>Prevent fraud and abuse</li>
  </ul>
  <p style="color: #000000;">Google may collect information such as your IP address, browser type, and browsing history. This information is subject to Google's Privacy Policy, which you can review at <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">https://policies.google.com/privacy</a>.</p>
  <p style="color: #000000;">You can opt out of personalized advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google's Ad Settings</a> or using browser extensions like AdBlock.</p>

  <h3 style="color: #000000; margin-top: 24px;">Analytics</h3>
  <p style="color: #000000;">We may use Google Analytics or similar tools to analyze website traffic and user behavior. These services may collect anonymized data about your visits.</p>

  <h2 style="color: #000000; margin-top: 32px;">Cookies Policy</h2>
  <p style="color: #000000;">Cookies are small text files stored on your device when you visit our website. We use cookies for:</p>
  <ul style="color: #000000;">
    <li><strong>Essential Cookies:</strong> Required for the website to function properly</li>
    <li><strong>Analytics Cookies:</strong> Help us understand how visitors use our site</li>
    <li><strong>Advertising Cookies:</strong> Used by Google AdSense to deliver relevant ads</li>
  </ul>
  <p style="color: #000000;">You can control cookie settings through your browser preferences. Note that disabling cookies may affect website functionality.</p>

  <h2 style="color: #000000; margin-top: 32px;">Data Security</h2>
  <p style="color: #000000;">We implement appropriate technical and organizational measures to protect your personal data against unauthorized access, alteration, disclosure, or destruction. However, no method of transmission over the internet is 100% secure.</p>

  <h2 style="color: #000000; margin-top: 32px;">Your Rights</h2>
  <p style="color: #000000;">Depending on your location, you may have the following rights regarding your personal data:</p>
  <ul style="color: #000000;">
    <li>Access your personal data</li>
    <li>Correct inaccurate data</li>
    <li>Request deletion of your data</li>
    <li>Object to processing of your data</li>
    <li>Data portability</li>
    <li>Opt-out of marketing communications</li>
  </ul>
  <p style="color: #000000;">To exercise these rights, please contact us at <a href="mailto:admin@mytribal.ai">admin@mytribal.ai</a>.</p>

  <h2 style="color: #000000; margin-top: 32px;">Children's Privacy</h2>
  <p style="color: #000000;">Our website is not intended for children under 13 years of age. We do not knowingly collect personal information from children under 13.</p>

  <h2 style="color: #000000; margin-top: 32px;">Changes to This Policy</h2>
  <p style="color: #000000;">We may update this privacy policy from time to time. We will notify you of any material changes by posting the new policy on this page and updating the "Last updated" date.</p>

  <h2 style="color: #000000; margin-top: 32px;">Contact Us</h2>
  <p style="color: #000000;">If you have questions about this privacy policy or our data practices, please contact us:</p>
  <p style="color: #000000;">
    <strong>Email:</strong> <a href="mailto:admin@mytribal.ai">admin@mytribal.ai</a><br>
    <strong>Website:</strong> <a href="https://mytribal.ai">https://mytribal.ai</a>
  </p>

  <p style="margin-top: 48px; color: #666666; font-size: 0.9em;">© {year} MyTribal AI. All rights reserved.</p>
</div>
""".strip()


def create_or_update_privacy_policy_page():
    auth = create_auth_header()
    if not auth:
        print("❌ Missing WP credentials. Set WP_USERNAME and WP_APP_PASSWORD in your environment.")
        return False

    headers = {
        'Authorization': auth,
        'Content-Type': 'application/json',
    }

    content_html = build_privacy_policy_content()
    title = "Privacy Policy"
    slug = "privacy-policy"

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
                print(f"✅ Updated Privacy Policy page (ID: {page_id})")
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
                print(f"✅ Created Privacy Policy page (ID: {data.get('id')})")
                return True
            else:
                print(f"❌ Failed to create page: {resp.status_code}")
                print(resp.text[:300])
                return False
    except Exception as e:
        print(f"❌ Error creating/updating Privacy Policy page: {e}")
        return False


def main():
    print("🚀 Creating/Updating Privacy Policy page on WordPress...")
    ok = create_or_update_privacy_policy_page()
    if ok:
        print(f"🌐 Visit: {WP_URL}/privacy-policy/")
    else:
        print("⚠️ Operation not completed.")


if __name__ == "__main__":
    main()


