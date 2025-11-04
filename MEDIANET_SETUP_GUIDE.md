# Media.net Setup Guide for WordPress

Complete guide to set up Media.net and replace Ezoic on your WordPress site.

## Step 1: Apply to Media.net (Contact Method)

### Application Process:
Media.net now requires direct contact instead of online sign-up:

1. **Contact Options:**
   - **Email:** publishers@media.net
   - **Contact Page:** https://www.media.net/contact/
   - **Publisher Page:** https://www.media.net/ads/publisher-program/

2. **Send Application Email:**
   - Subject: Publisher Application - mytribal.ai
   - Include in email:
     - Website URL: `https://mytribal.ai`
     - Your email address
     - Your name
     - Phone number (optional)
     - Website category: Technology/AI
     - Monthly page views: Your current traffic
     - Content description: AI/tech news and analysis
     - Why you're interested in Media.net

3. **Email Template (copy below):**
```
Subject: Publisher Application - mytribal.ai

Hello Media.net Team,

I would like to apply to become a publisher with Media.net.

Website Details:
- URL: https://mytribal.ai
- Category: Technology / Artificial Intelligence
- Monthly Page Views: [Your number]
- Content: AI and technology news, analysis, and insights

My site focuses on artificial intelligence, machine learning, and tech industry 
news. I publish daily high-quality articles (1000-1500 words) with original 
analysis and insights.

I have:
- Privacy Policy page
- About Us page  
- Contact page
- Navigation menu
- 30+ quality posts
- Active publishing schedule

Please let me know if you need any additional information.

Thank you,
[Your Name]
[Your Email]
```

4. **Wait for Response:**
   - Usually 4-5 business days
   - They'll send email with approval and dashboard access

### Approval Criteria:
- ✅ Active website (you have this!)
- ✅ Original content (your AI/tech articles)
- ✅ Privacy Policy (you have this!)
- ✅ Decent traffic (they're more lenient than AdSense)

## Step 2: Get Your Media.net Ad Code

After approval:
1. **Log into Media.net Dashboard:** https://dashboard.media.net
2. **Go to:** "Ad Units" or "Create Ad Unit"
3. **Choose ad types:**
   - **Display Ads** (banner ads)
   - **Native Ads** (content-integrated)
   - **Sticky Ads** (optional)
   
4. **Configure each ad unit:**
   - Name: e.g., "Leaderboard Top", "Sidebar 300x250", "Native In-Content"
   - Size: 728x90, 300x250, 300x600, etc.
   - Placement: Select where it will appear

5. **Generate Ad Code:**
   - Media.net will provide JavaScript code
   - Copy each ad unit code
   - Save them (we'll use these in WordPress)

## Step 3: Deactivate Ezoic Plugin

### Before You Start:
- Make sure you have Media.net ad codes ready
- Or temporarily remove ads if switching

### Steps to Deactivate:
1. **Log into WordPress Admin:**
   - Go to: `https://mytribal.ai/wp-admin`

2. **Navigate to Plugins:**
   - Click: `Plugins` → `Installed Plugins` (left sidebar)

3. **Find Ezoic Plugin:**
   - Look for: "Ezoic" or "Ezoic Integration" or similar
   - Plugins might include:
     - Ezoic
     - Ezoic Speed
     - Ezoic Ad Tester
     - Ezoic Cloudflare

4. **Deactivate Ezoic:**
   - Click: `Deactivate` under each Ezoic plugin
   - Or select multiple → `Bulk Actions` → `Deactivate`

5. **Optional - Remove Ezoic:**
   - After deactivating, you can click `Delete` to remove completely
   - **Warning:** This removes the plugin files (you can reinstall later if needed)

6. **Clear Cache:**
   - If you use caching plugins, clear cache
   - Clear browser cache too

## Step 4: Install Media.net on WordPress

### Option A: Using Insert Headers and Footers Plugin (Recommended)

1. **Install Plugin:**
   - Go to: `Plugins` → `Add New`
   - Search: "Insert Headers and Footers"
   - Install: "Insert Headers and Footers" by WPBeginner
   - Activate the plugin

2. **Add Media.net Script:**
   - Go to: `Settings` → `Insert Headers and Footers`
   - In "Scripts in Header" box, paste Media.net verification code
   - Save changes

3. **Add Ad Units:**
   - Use widget areas or ad plugins (see Option B below)

### Option B: Using Ad Inserter Plugin (Better Control)

1. **Install Plugin:**
   - Go to: `Plugins` → `Add New`
   - Search: "Ad Inserter"
   - Install: "Ad Inserter" by spacetime
   - Activate

2. **Add Media.net Ad Units:**
   - Go to: `Settings` → `Ad Inserter`
   - Click: "Add Block" for each ad unit
   - Name each block: "Header Ad", "Sidebar Ad", "Content Ad", etc.
   - Paste Media.net ad code in the "Ad code" box
   - Set insertion settings:
     - **Header Ad:** Before post (automatic)
     - **Sidebar Ad:** In widget area
     - **Content Ad:** Between paragraphs

3. **Configure Positions:**
   - Use the visual editor to place ads
   - Set paragraph numbers for in-content ads (e.g., after paragraph 3)

### Option C: Manual Placement (Advanced)

1. **Edit Theme Files:**
   - Go to: `Appearance` → `Theme Editor`
   - Edit `header.php` for header ads
   - Edit `sidebar.php` for sidebar ads
   - Edit `single.php` or `content.php` for post content ads

2. **Add Ad Code:**
   - Paste Media.net JavaScript code where you want ads
   - Save files

⚠️ **Warning:** Editing theme files directly can break your site. Always backup first!

## Step 5: Common Ad Placements

### Recommended Placements:
1. **Top of Posts:** 728x90 or 970x90 (Leaderboard)
2. **Sidebar:** 300x250 (Medium Rectangle)
3. **In-Content:** Native ads or 300x250
4. **Bottom of Posts:** 728x90 or Native ads
5. **Sticky Sidebar:** 300x600 (optional)

### Best Practices:
- ✅ Don't place too many ads (hurts user experience)
- ✅ 3-5 ads per page is optimal
- ✅ Native ads perform better than banners
- ✅ Mobile-responsive ad sizes

## Step 6: Verify Installation

1. **Check Media.net Dashboard:**
   - Log into: https://dashboard.media.net
   - Look for "Active Ad Units" or "Ad Status"
   - Should show ads are live

2. **Test Your Site:**
   - Visit your homepage: https://mytribal.ai
   - Visit a post page
   - Check if ads are displaying
   - Test on mobile too

3. **Browser Tools:**
   - Right-click → Inspect Element
   - Look for Media.net scripts in page source
   - Check for ad containers

## Step 7: Monitor Performance

1. **Media.net Dashboard:**
   - Check daily/weekly performance
   - Monitor RPM (Revenue Per 1000 impressions)
   - Check fill rate
   - Optimize ad placements

2. **WordPress:**
   - Monitor site speed (ads can slow sites)
   - Check user experience
   - Review bounce rates

## Troubleshooting

### Ads Not Showing?
- ✅ Check ad code is correctly pasted
- ✅ Verify Media.net account is approved
- ✅ Clear WordPress cache
- ✅ Clear browser cache
- ✅ Check ad blocker (disable for testing)
- ✅ Wait 24-48 hours (ads may take time to propagate)

### Site Speed Issues?
- ✅ Use lazy loading for ads
- ✅ Limit number of ad units
- ✅ Use async ad loading
- ✅ Consider CDN

### Need Help?
- Media.net Support: support@media.net
- Check Media.net knowledge base
- WordPress forums for plugin-specific issues

## Quick Reference

**Media.net Dashboard:** https://dashboard.media.net
**Media.net Publisher Portal:** https://www.media.net/publishers/
**WordPress Admin:** https://mytribal.ai/wp-admin

---

## Checklist

- [ ] Applied for Media.net account
- [ ] Received approval email
- [ ] Created ad units in Media.net dashboard
- [ ] Copied ad codes
- [ ] Deactivated Ezoic plugins
- [ ] Installed WordPress plugin (Ad Inserter or Insert Headers/Footers)
- [ ] Added Media.net ad codes
- [ ] Placed ads in strategic locations
- [ ] Verified ads are displaying
- [ ] Tested on mobile
- [ ] Monitored performance

---

**Next Steps:** Once Media.net is set up and running, you can focus on building traffic and content. The combination of Media.net + Amazon Associates should provide good monetization while you wait for AdSense reconsideration.

