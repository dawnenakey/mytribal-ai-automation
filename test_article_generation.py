#!/usr/bin/env python3
"""
Quick test to verify the improved article generation works.
Tests if articles are now 1000+ words and properly formatted.
"""

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("❌ OPENAI_API_KEY not found in .env file")
    exit(1)

try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    print("🧪 Testing improved article generation...")
    print("="*70)
    
    test_title = "Apple Announces New AI Partnerships Strategy"
    test_description = "Apple CEO Tim Cook says the company is open to M&A on the AI front, preparing to announce more AI partnerships similar to the OpenAI integration."
    
    prompt = f"""
        Create a comprehensive, in-depth blog post about this AI/tech topic:
        
        Title: {test_title}
        Description: {test_description}
        
        CRITICAL REQUIREMENTS FOR ADSENSE QUALITY:
        
        LENGTH & DEPTH:
        - Write 1000-1500 words minimum (substantial, valuable content)
        - Go beyond summaries - provide deep analysis and insights
        - Include original perspective and expert commentary
        - Add context, background, and detailed explanations
        
        CONTENT QUALITY:
        - Write from the perspective of a data scientist with expertise in AI/ML
        - Include your own analysis, not just reporting
        - Add practical insights, implications, and real-world applications
        - Discuss the "why" and "how" behind the topic, not just "what"
        - Include relevant data, statistics, or research when applicable
        
        STRUCTURE & FORMATTING (REQUIRED):
        - Start with an engaging introduction (150-200 words)
        - Use H2 headings for main sections (at least 4-5 sections)
        - Use H3 headings for subsections within main sections
        - Include bullet points or numbered lists where appropriate
        - Break content into readable paragraphs (3-5 sentences each)
        - Add a conclusion section with key takeaways
        
        WRITING STYLE:
        - Write in first person or third person - NEVER mention "as an AI" or AI limitations
        - Sound like a human expert, not a chatbot
        - Be authoritative but accessible
        - Use engaging, clear language
        - Avoid generic phrases - be specific and original
        
        UNIQUE VALUE ADDITIONS:
        - Explain implications for the industry
        - Discuss potential impact on businesses/developers
        - Add your professional insights from a data science perspective
        - Include practical applications or use cases
        - Connect to broader trends or patterns
        - Add forward-looking analysis where relevant
        
        ENGAGEMENT:
        - Include a call-to-action at the end
        - Ask thought-provoking questions
        - Encourage discussion and further exploration
        
        Format the response as clean HTML with:
        - <h2> for main section headings (use at least 4-5)
        - <h3> for subsection headings
        - <p> tags for paragraphs
        - <ul> or <ol> for lists
        - <strong> for emphasis where appropriate
        
        Write comprehensively and authoritatively. This must be high-quality, valuable content that provides real insights, not just a summary.
        """
    
    print(f"\n📝 Generating test article...")
    print(f"   Title: {test_title}")
    print("   Please wait (this may take 30-60 seconds)...\n")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an experienced tech writer and data scientist with a Master's degree in Data Science from University of Denver. You write comprehensive, insightful articles about AI and technology that provide real value to readers. You never mention being an AI or AI limitations - you write as a human expert."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000,
        temperature=0.8
    )
    
    article = response.choices[0].message.content.strip()
    
    # Analyze the article
    word_count = len(article.split())
    has_h2 = '<h2' in article.lower()
    has_h3 = '<h3' in article.lower()
    has_lists = '<ul' in article.lower() or '<ol' in article.lower()
    no_ai_phrases = not any(phrase in article.lower() for phrase in ['as an ai', 'i am an ai', 'i cannot', 'as a large language model'])
    
    print("="*70)
    print("TEST RESULTS")
    print("="*70)
    print(f"\n✅ Word Count: {word_count} words")
    if word_count >= 1000:
        print("   ✅ Meets AdSense requirement (1000+ words)")
    else:
        print(f"   ❌ Too short - needs {1000 - word_count} more words")
    
    print(f"\n📋 Structure:")
    print(f"   H2 Headings: {'✅ Found' if has_h2 else '❌ Missing'}")
    print(f"   H3 Headings: {'✅ Found' if has_h3 else '⚠️ Missing (recommended)'}")
    print(f"   Lists: {'✅ Found' if has_lists else '⚠️ Missing (recommended)'}")
    
    print(f"\n✍️ Writing Quality:")
    print(f"   No AI disclaimers: {'✅ Good' if no_ai_phrases else '❌ Contains AI phrases'}")
    
    # Count headings
    h2_count = article.lower().count('<h2')
    h3_count = article.lower().count('<h3')
    
    print(f"\n📊 Detailed Structure:")
    print(f"   H2 sections: {h2_count} ({'✅ Good' if h2_count >= 4 else '⚠️ Need 4-5'})")
    print(f"   H3 subsections: {h3_count} ({'✅ Good' if h3_count >= 2 else '⚠️ Recommended'})")
    
    print("\n" + "="*70)
    
    if word_count >= 1000 and has_h2 and no_ai_phrases:
        print("✅ SUCCESS! Article generation is working correctly.")
        print("   Your automation will now produce AdSense-quality content!")
    else:
        print("⚠️ Some issues detected. Article may need adjustment.")
    
    print("\n📄 First 500 characters of generated article:")
    print("-"*70)
    print(article[:500] + "...")
    print("="*70)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

