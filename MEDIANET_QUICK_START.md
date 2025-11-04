# Media.net Quick Start Guide

## ⚡ Fast Track Setup (5 Steps)

### Step 1: Apply to Media.net (5 minutes)
1. Go to: https://www.media.net/publishers/
2. Click "Sign Up"
3. Enter your site: `mytribal.ai`
4. Fill out the form
5. Submit

**Wait:** 1-3 business days for approval

---

### Step 2: Deactivate Ezoic (2 minutes)
1. Log in: https://mytribal.ai/wp-admin
2. Go to: `Plugins` → `Installed Plugins`
3. Find all "Ezoic" plugins
4. Click `Deactivate` on each
5. (Optional) Click `Delete` to remove

**Done!** Ezoic is removed.

---

### Step 3: Get Media.net Ad Code (After Approval)
1. Log into: https://dashboard.media.net
2. Go to: `Ad Units` → `Create New Ad Unit`
3. Create these ad sizes:
   - **728x90** (Leaderboard - top of posts)
   - **300x250** (Medium Rectangle - sidebar)
   - **Native Ad** (in-content)
4. Copy each ad code
5. Save them somewhere (text file or notes)

---

### Step 4: Install Ad Plugin (3 minutes)
1. In WordPress: `Plugins` → `Add New`
2. Search: **"Ad Inserter"**
3. Install: "Ad Inserter" by spacetime
4. Click `Activate`

---

### Step 5: Add Media.net Ads (5 minutes)
1. Go to: `Settings` → `Ad Inserter`
2. For each ad unit:
   - Click `Add Block`
   - Name it (e.g., "Header Ad")
   - Paste Media.net code
   - Set position:
     - Header: `Before content`
     - Sidebar: `Widget area` (then add to sidebar widget)
     - Content: `After paragraph 3`
3. Click `Save`

**Done!** Ads are live.

---

## 🎯 Recommended Ad Placements

1. **Top of Posts:** 728x90 Leaderboard
2. **Sidebar:** 300x250 Rectangle  
3. **In-Content (after para 3):** Native ad or 300x250
4. **Bottom of Posts:** Native ad

**Total:** 3-4 ads per post (optimal for revenue + UX)

---

## 📞 Need Help?

- **Media.net Support:** support@media.net
- **Full Guide:** See `MEDIANET_SETUP_GUIDE.md`
- **Removal Help:** See `remove_ezoic_from_wordpress.py`

---

## ✅ Checklist

- [ ] Applied to Media.net
- [ ] Deactivated Ezoic plugins
- [ ] Received Media.net approval
- [ ] Created ad units in Media.net
- [ ] Installed Ad Inserter plugin
- [ ] Added ad codes to WordPress
- [ ] Verified ads are showing
- [ ] Tested on mobile

---

**Estimated Time:** 15-20 minutes (plus 1-3 days for Media.net approval)

