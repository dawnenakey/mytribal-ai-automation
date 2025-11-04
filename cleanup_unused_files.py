#!/usr/bin/env python3
"""
Identify and optionally remove unused files in the repository.
"""

import os
from pathlib import Path

# Core scripts that are actively used
CORE_SCRIPTS = {
    'daily_automation.py',  # Main automation
    'daily_ai_content_generator.py',  # Content generation
    'wordpress_rest_publisher.py',  # Publishing
    'create_services_page.py',  # Services page
    'create_case_studies_page.py',  # Case studies page
    'create_about_page.py',  # About page
    'create_contact_page.py',  # Contact page
    'create_privacy_policy_page.py',  # Privacy policy
}

# Utility scripts that are one-time use but should be kept
UTILITY_SCRIPTS = {
    'add_pages_to_navigation.py',
    'add_to_main_navigation.py',
    'check_website_pages.py',
    'check_content_quality.py',
    'check_navigation_structure.py',
    'check_and_fix_menu.py',
    'fix_navigation_block_theme.py',
    'test_article_generation.py',
    'cleanup_unused_files.py',  # This script itself
}

# Config/template files to keep
CONFIG_FILES = {
    'requirements.txt',
    'env_template.txt',
    '.env',
    '.gitignore',
    'setup_cron.sh',
    'com.mytribal.automation.plist',
}

# Documentation files to keep
DOC_FILES = {
    'README.md',
    'QUICK_START_GUIDE.md',
    'AUTOMATION_SETUP.md',
    'TROUBLESHOOTING.md',
    'ADSENSE_APPROVAL_GUIDE.md',
    'ADSENSE_PRE_SUBMISSION_CHECKLIST.md',
    'IMPROVED_CONTENT_GUIDE.md',
    'access_site_editor_guide.md',
    'fix_block_theme_navigation.md',
}

# Directories to keep
KEEP_DIRECTORIES = {
    'content_for_mytribal',
    'rss_data',
    'rss_data_enhanced',
}

# Potentially unused files (old/deprecated)
POTENTIALLY_UNUSED = {
    'scheduler.py',  # May be replaced by cron
    'mytribal_rss_daily.log',
    'mytribal_rss_enhanced.log',
    'mytribal_rss.log',
    'publish_to_mytribal.log',
    'mytribal_rss_data.json',
    'social_media_posts.txt',
    'mytribal-store.html',
    'product-template-small-business-marketing-kit.html',
}

# Log files (can be regenerated)
LOG_FILES = {
    'automation.log',
    'daily_automation.log',
    'daily_ai_content_generator.log',
    'cron_test.log',
    'mytribal_rss_daily.log',
    'mytribal_rss_enhanced.log',
    'mytribal_rss.log',
    'publish_to_mytribal.log',
}

def analyze_files():
    """Analyze repository and identify unused files."""
    repo_path = Path('.')
    all_files = {f.name for f in repo_path.iterdir() if f.is_file()}
    
    keep_files = CORE_SCRIPTS | UTILITY_SCRIPTS | CONFIG_FILES | DOC_FILES
    
    unused_files = []
    for file in all_files:
        if file not in keep_files and file not in LOG_FILES:
            # Check if it's a log file pattern
            if file.endswith('.log'):
                continue
            # Check if it's in a keep directory
            if any(Path(file).parent.name == d for d in KEEP_DIRECTORIES):
                continue
            unused_files.append(file)
    
    print("="*70)
    print("FILE CLEANUP ANALYSIS")
    print("="*70)
    
    print(f"\n✅ Core Scripts ({len(CORE_SCRIPTS)} files):")
    for f in sorted(CORE_SCRIPTS):
        if Path(f).exists():
            print(f"   ✓ {f}")
        else:
            print(f"   ✗ {f} (not found)")
    
    print(f"\n🔧 Utility Scripts ({len(UTILITY_SCRIPTS)} files):")
    for f in sorted(UTILITY_SCRIPTS):
        if Path(f).exists():
            print(f"   ✓ {f}")
    
    print(f"\n⚠️ Potentially Unused Files ({len(POTENTIALLY_UNUSED)} files):")
    for f in sorted(POTENTIALLY_UNUSED):
        if Path(f).exists():
            print(f"   ? {f}")
    
    print(f"\n📝 Log Files ({len(LOG_FILES)} files - can be deleted):")
    for f in sorted(LOG_FILES):
        if Path(f).exists():
            size = Path(f).stat().st_size
            print(f"   🗑️  {f} ({size} bytes)")
    
    print(f"\n❓ Other Files Not in Categories:")
    other_files = all_files - keep_files - POTENTIALLY_UNUSED - LOG_FILES
    for f in sorted(other_files):
        if not f.startswith('.'):
            print(f"   ? {f}")
    
    print("\n" + "="*70)
    print("RECOMMENDATIONS")
    print("="*70)
    
    print("\n🗑️ SAFE TO DELETE (log files - can be regenerated):")
    for f in sorted(LOG_FILES):
        if Path(f).exists():
            print(f"   - {f}")
    
    print("\n⚠️ REVIEW BEFORE DELETING:")
    print("   - scheduler.py (if using cron instead)")
    print("   - mytribal_rss_data.json (old RSS data)")
    print("   - mytribal-store.html (if not needed)")
    print("   - product-template-small-business-marketing-kit.html (if not needed)")
    print("   - social_media_posts.txt (if not needed)")
    
    print("\n" + "="*70)
    
    return LOG_FILES, POTENTIALLY_UNUSED

if __name__ == "__main__":
    logs, unused = analyze_files()
    
    print("\n💡 To clean up log files, run:")
    print("   rm *.log")
    print("\n💡 To remove potentially unused files, manually review and delete.")

