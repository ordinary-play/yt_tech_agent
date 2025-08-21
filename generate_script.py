import os, sys, json, re
from dotenv import load_dotenv
from storage import init_db, save_script
from fetch_trends import fetch_all_trends

# SDKs
from openai import OpenAI
import anthropic
import google.generativeai as genai

load_dotenv()

# Load keys
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# --- Optimized Prompt ---
SCRIPT_PROMPT_TEMPLATE = """
You are a YouTube script writer for tech content. 
Write a complete YouTube video script in this exact structure:

1. Title  
   - Short, clickable, engaging.

2. Hook (first 10–15 sec, written as spoken dialogue)  
   - Attention-grabbing statement that creates curiosity.

3. Narration Flow (with timestamps, clear breakdown)  
   - [0:00–0:45] The Report → Quick summary of the issue.  
   - [0:45–2:00] Analysis → Explain reasons behind the issue.  
   - [2:00–3:00] Case Studies → At least one failed example and one success story.  
   - [3:00–4:00] Expectation vs. Reality → Contrast hype vs. actual outcome.  
   - [4:00–5:00] Implications → What it means for the audience or investors.  

4. CTA (Call to Action, at end only)  
   - Suggest subscribing, liking, or following for more tech updates.

5. Description (SEO-optimized, first 2 lines very strong)  
   - Concise summary that boosts search ranking.  

Rules:  
- Use natural, conversational tone (like speaking to humman).  
- Strictly follow the above structure.  
- Do not add extra explanation outside the script.
-use simple english.
"""

def safe_text(text):
    """Clean model text if needed"""
    return re.sub(r"^```.*?json|```$", "", text.strip(), flags=re.DOTALL)

def call_openai(prompt):
    client = OpenAI(api_key=OPENAI_KEY)
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000,
    )
    return safe_text(r.choices[0].message.content)

def call_anthropic(prompt):
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    r = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}],
    )
    return safe_text(r.content[0].text)

def call_gemini(prompt):
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    resp = model.generate_content(prompt)
    return safe_text(resp.text)

def generate_script_for(topic: str):
    final_prompt = SCRIPT_PROMPT_TEMPLATE + f"\n\nTopic: {topic}"

    try:
        if OPENAI_KEY:
            print("Just a seconds...")
            return call_openai(final_prompt)
    except Exception as e:
        print("OpenAI failed:", e)

    try:
        if ANTHROPIC_KEY:
            print("Please Wait...")
            return call_anthropic(final_prompt)
    except Exception as e:
        print("Anthropic failed:", e)

    try:
        if GEMINI_KEY:
            print("Wait...")
            return call_gemini(final_prompt)
    except Exception as e:
        print("Gemini failed:", e)

    return f"Topic: {topic}\nNo provider responded."

if __name__ == "__main__":
    # Allow manual topic override
    if len(sys.argv) > 1:
        chosen_topic = " ".join(sys.argv[1:])
        print(f"\nManual topic provided: {chosen_topic}\n")
    else:
        print("Fetching trending topics...")
        topics = fetch_all_trends()
        if not topics:
            print("No topics found.")
            raise SystemExit(1)
        chosen_topic = topics[0]
        print(f"\nTrending topic chosen: {chosen_topic}\n")

    script_text = generate_script_for(chosen_topic)

    # Save raw script into DB
    conn = init_db("data.db")
    sid = save_script(conn, chosen_topic, {"title": chosen_topic, "script": script_text})
    conn.close()

    print("\n--- YouTube Script Output ---")
    print("Saved to database with ID:", sid)
    print(script_text)
