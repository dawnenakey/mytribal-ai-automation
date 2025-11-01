#!/usr/bin/env python3
"""
Create or update the Home page on WordPress from ./web/index.html
- Uses WP REST API with Basic Auth (username + application password)
- If SET_AS_HOMEPAGE=true, sets the created/updated page as the front page

Required env vars:
  WP_URL=https://mytribal.ai
  WP_USERNAME=your-wp-admin-username
  WP_APP_PASSWORD=your-application-password
Optional:
  SET_AS_HOMEPAGE=true|false   (default true)

NOTE: This script removes <script>...</script> tags before publishing
because WordPress will usually strip them unless the user has
unfiltered_html capability. We also stamp the © year server-side.
"""

import os, json, base64, ssl, pathlib, re
from datetime import datetime
import requests
from dotenv import load_dotenv
import urllib3

# -------- Config / Env
load_dotenv()
WP_URL = os.getenv("WP_URL", "https://mytribal.ai").rstrip("/")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")
SET_AS_HOMEPAGE = os.getenv("SET_AS_HOMEPAGE", "true").lower() in ("1", "true", "yes")

HTML_PATH = pathlib.Path("web/index.html")
PAGE_TITLE = "Home"
PAGE_SLUG = "home"

# -------- Helpers
def _auth_header():
    if not WP_USERNAME or not WP_APP_PASSWORD:
        raise RuntimeError("Missing WP credentials. Set WP_USERNAME and WP_APP_PASSWORD.")
    token = base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
    return {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

def _wp_get(url):
    headers = _auth_header()
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    return requests.get(url, headers=headers, verify=False, timeout=30)

def _wp_post(url, payload):
    headers = _auth_header()
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    return requests.post(url, headers=headers, data=json.dumps(payload), verify=False, timeout=60)

def get_page_by_slug(slug: str):
    r = _wp_get(f"{WP_URL}/wp-json/wp/v2/pages?slug={slug}")
    if r.status_code != 200:
        raise RuntimeError(f"Search page failed {r.status_code}: {r.text[:200]}")
    pages = r.json()
    return pages[0] if pages else None

def clean_html_for_wp(raw_html: str) -> str:
    """Remove <script>...</script> and stamp the year to avoid WP stripping."""
    # Stamp © year (your HTML already has an element for it; we replace server-side)
    current_year = str(datetime.now().year)
    stamped = raw_html.replace('© <span id="year"></span>', f'© {current_year}')

    # Strip any <script> blocks (WP will sanitize; we make it explicit)
    no_scripts = re.sub(r"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>", "", stamped, flags=re.IGNORECASE)
    return no_scripts

def upsert_page(title: str, slug: str, content_html: str) -> int:
    existing = get_page_by_slug(slug)
    payload = {"title": title, "content": content_html, "status": "publish"}

    if existing:
        page_id = existing["id"]
        r = _wp_post(f"{WP_URL}/wp-json/wp/v2/pages/{page_id}", payload)
        if r.status_code != 200:
            raise RuntimeError(f"Update failed {r.status_code}: {r.text[:300]}")
        print(f"✅ Updated Home page (ID: {page_id})")
        return page_id
    else:
        payload.update({"slug": slug})
        r = _wp_post(f"{WP_URL}/wp-json/wp/v2/pages", payload)
        if r.status_code != 201:
            raise RuntimeError(f"Create failed {r.status_code}: {r.text[:300]}")
        page_id = r.json()["id"]
        print(f"✅ Created Home page (ID: {page_id})")
        return page_id

def set_as_front_page(page_id: int):
    """Requires manage_options capability (Admin)."""
    r = _wp_post(f"{WP_URL}/wp-json/wp/v2/settings",
                 {"show_on_front": "page", "page_on_front": page_id})
    if r.status_code != 200:
        raise RuntimeError(f"Failed to set homepage {r.status_code}: {r.text[:300]}")
    print("🏠 Set as site homepage.")

# -------- Main
def main():
    if not HTML_PATH.exists():
        raise FileNotFoundError("web/index.html not found. Create it and try again.")

    raw_html = HTML_PATH.read_text(encoding="utf-8")
    html = clean_html_for_wp(raw_html)

    page_id = upsert_page(PAGE_TITLE, PAGE_SLUG, html)
    if SET_AS_HOMEPAGE:
        try:
            set_as_front_page(page_id)
        except Exception as e:
            # Not fatal—user may not have permissions
            print(f"⚠️ Could not set as homepage via API: {e}\n   You can set it in WP Admin → Settings → Reading.")

    print(f"🌐 View your page: {WP_URL}/")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"❌ {exc}")
        raise