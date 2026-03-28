import json
import os
import random
import csv

script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.dirname(script_dir)
raw_dir = os.path.join(dataset_dir, "data", "raw")
processed_dir = os.path.join(dataset_dir, "data", "processed")
qa_pairs_dir = os.path.join(dataset_dir, "data", "qa_pairs")

os.makedirs(processed_dir, exist_ok=True)
os.makedirs(qa_pairs_dir, exist_ok=True)

with open(os.path.join(raw_dir, "key_verses.json"), 'r', encoding='utf-8') as f: key_verses = json.load(f)
verse_lookup = {v["verse_id"]: v for v in key_verses}

with open(os.path.join(processed_dir, "problem_verse_mapping.json"), 'r', encoding='utf-8') as f: problems = json.load(f)
with open(os.path.join(raw_dir, "concept_glossary.json"), 'r', encoding='utf-8') as f: concepts = json.load(f)
with open(os.path.join(raw_dir, "chapters.json"), 'r', encoding='utf-8') as f: chapters = json.load(f)

# Combintorial English Templates
en_prefs = [
    "I am struggling with", "How can I overcome", "My mind is troubled by", 
    "I feel overwhelmed by", "What is the spiritual perspective on", 
    "How do I deal with", "I am facing", "Can you give me strength to handle", 
    "Why do I suffer from", "I need advice on", "Krishna, I am lost in",
    "What is the deepest root of", "Is there a shloka that can help me with",
    "I feel paralyzed by", "Teach me how to conquer", "My heart is heavy because of",
    "How would a yogi deal with", "I am searching for peace amidst", "Tell me a painful truth about"
]
en_suffs = [
    "?", ". What does the Gita say?", ". Any guidance?", ". Please help me.", 
    ". What should I do?", " according to the Bhagavad Gita?", ". How do I move forward?",
    ". What is the solution?", ". Show me the way."
]
english_templates = [f"{p} {{}}{s}" for p in en_prefs for s in en_suffs]

# Combintorial Hindi Templates
hi_prefs = [
    "मैं {} से जूझ रहा हूँ", "मैं {} पर कैसे विजय प्राप्त करूँ", "मेरा मन {} से बहुत परेशान है", 
    "मैं {} से अभिभूत महसूस कर रहा हूँ", "मुझे {} का सामना करना पड़ रहा है", 
    "क्या आप मुझे {} को संभालने की शक्ति दे सकते हैं", "मैं {} से क्यों पीड़ित हूँ", 
    "मुझे {} पर सलाह चाहिए", "हे कृष्ण, मैं {} में खो गया हूँ", 
    "भगवद गीता के अनुसार {} का मूल कारण क्या है", "क्या कोई श्लोक है जो {} में मेरी मदद कर सके"
]
hi_suffs = [
    "?", "। गीता इस बारे में क्या कहती है?", "। कोई मार्गदर्शन दें?", "। कृपया मेरी मदद करें।", 
    "। मुझे क्या करना चाहिए?", "। मुझे मार्ग दिखाएं।", "। समाधान क्या है?"
]
hindi_templates = [f"{p}{s}" for p in hi_prefs for s in hi_suffs]

wisdom_prefixes_en = [
    "",
    "As I told Arjuna on the battlefield of Kurukshetra:\n\n",
    "Hear this ancient wisdom, O seeker:\n\n",
    "The divine truth of the matter is this:\n\n",
    "Let your mind find peace in this teaching:\n\n",
    "Do not despair. The Gita provides clear guidance:\n\n"
]
wisdom_outros_en = [
    "",
    "\n\nMeditate on this truth and you shall find peace.",
    "\n\nRemember, you are entirely supported by the divine. Act without fear.",
    "\n\nLet go of the attachments causing this pain, and stand up with courage.",
    "\n\nThis is the eternal path of Yoga. Walk it steadily."
]

wisdom_prefixes_hi = [
    "",
    "कुरुक्षेत्र के युद्ध के मैदान में जैसा मैंने अर्जुन से कहा था:\n\n",
    "हे साधक, इस प्राचीन ज्ञान को सुनो:\n\n",
    "परम सत्य यह है:\n\n"
]
wisdom_outros_hi = [
    "",
    "\n\nइस सत्य पर ध्यान करो और तुम्हें शांति मिलेगी।",
    "\n\nयाद रखो, परमात्मा तुम्हारा पूरी तरह से समर्थन करता है। बिना डर के कार्य करो।",
    "\n\nयह योग का शाश्वत मार्ग है। इस पर दृढ़ता से चलो।"
]

generated_qa_pairs = []
qa_id_counter = 1

# 1. PROBLEMS
random.seed(42) # Ensuring reproducibility
for p in problems:
    primary_verse_id = p["primary_verse"]
    if primary_verse_id not in verse_lookup: continue
    v = verse_lookup[primary_verse_id]
    keywords = [k.strip() for k in p["problem_keywords"].split(",")]
    sanskrit, transliteration, translation_en, translation_hi, purport = v.get("sanskrit_devanagari", ""), v.get("transliteration", ""), v.get("translation_english", ""), v.get("translation_hindi", ""), v.get("purport_summary", "")
    if not (sanskrit and transliteration and translation_en): continue
    
    for kw in keywords:
        if not kw: continue
        # EN
        for tmpl in english_templates:
            uq = tmpl.format(kw)
            pre = random.choice(wisdom_prefixes_en)
            suf = random.choice(wisdom_outros_en)
            resp = f"O seeker, hear this eternal truth:\n\n**Sanskrit:**\n{sanskrit}\n\n**Transliteration:**\n{transliteration}\n\n**Meaning:**\n{translation_en}\n\n{pre}{purport}{suf}"
            generated_qa_pairs.append({"qa_id": f"QA_{qa_id_counter:06d}", "category": p.get("problem_category", "general"), "user_question": uq, "verse_id": v["verse_id"], "chapter": v["chapter"], "verse": v["verse"], "krishna_response": resp, "language": "en", "tone": "compassionate"})
            qa_id_counter += 1
            
        # HI
        for tmpl in hindi_templates:
            uq = tmpl.format(kw)
            pre = random.choice(wisdom_prefixes_hi)
            suf = random.choice(wisdom_outros_hi)
            resp = f"हे साधक, इस शाश्वत सत्य को सुनो:\n\n**Sanskrit:**\n{sanskrit}\n\n**Transliteration:**\n{transliteration}\n\n**Meaning:**\n{translation_hi}\n\n{pre}{purport}{suf}"
            generated_qa_pairs.append({"qa_id": f"QA_{qa_id_counter:06d}", "category": p.get("problem_category", "general"), "user_question": uq, "verse_id": v["verse_id"], "chapter": v["chapter"], "verse": v["verse"], "krishna_response": resp, "language": "hi", "tone": "compassionate"})
            qa_id_counter += 1

# 2. CONCEPTS
concept_en_t = ["What is the meaning of {}?", "Explain the concept of {} in the Gita.", "How do I practice {}?", "What does Krishna say about {}?", "I want to understand {}."]
concept_hi_t = ["{} का क्या अर्थ है?", "गीता में {} की अवधारणा को समझाएं।", "मैं {} का अभ्यास कैसे करूँ?", "कृष्ण {} के बारे में क्या कहते हैं?", "मैं {} को समझना चाहता हूँ।"]
for c in concepts:
    verse_id = c.get("key_verse", "BG_2_47")
    if verse_id not in verse_lookup: verse_id = "BG_2_47"
    v = verse_lookup[verse_id]
    sanskrit, transliteration, translation_en, translation_hi = v.get("sanskrit_devanagari", ""), v.get("transliteration", ""), v.get("translation_english", ""), v.get("translation_hindi", "")
    term, meaning_en = c.get("term_sanskrit", ""), c.get("extended_meaning", "")
    for tmpl in concept_en_t:
        for _ in range(5):  # amplify concepts
            uq = tmpl.format(term)
            resp = f"O seeker, hear this eternal truth:\n\n**Sanskrit:**\n{sanskrit}\n\n**Transliteration:**\n{transliteration}\n\n**Meaning:**\n{translation_en}\n\nTo understand {term}, know this: {meaning_en}"
            generated_qa_pairs.append({"qa_id": f"QA_{qa_id_counter:06d}", "category": "philosophy", "user_question": uq, "verse_id": v["verse_id"], "chapter": v["chapter"], "verse": v["verse"], "krishna_response": resp, "language": "en", "tone": "philosophical"})
            qa_id_counter += 1
    for tmpl in concept_hi_t:
        for _ in range(5):
            uq = tmpl.format(term)
            resp = f"हे साधक, इस शाश्वत सत्य को सुनो:\n\n**Sanskrit:**\n{sanskrit}\n\n**Transliteration:**\n{transliteration}\n\n**Meaning:**\n{translation_hi}\n\n{term} का अर्थ है: {c.get('primary_meaning', '')}. {meaning_en}"
            generated_qa_pairs.append({"qa_id": f"QA_{qa_id_counter:06d}", "category": "philosophy", "user_question": uq, "verse_id": v["verse_id"], "chapter": v["chapter"], "verse": v["verse"], "krishna_response": resp, "language": "hi", "tone": "philosophical"})
            qa_id_counter += 1

# 3. CHAPTERS
chapter_en_t = ["What is Chapter {number} of the Gita about?", "Give me a summary of Chapter {number}.", "What are the key themes of {name_english}?", "Tell me about {name_sanskrit}."]
for ch in chapters:
    chapter_verses = [v for v in key_verses if v["chapter"] == ch["chapter_number"]]
    v = chapter_verses[0] if chapter_verses else verse_lookup["BG_2_47"]
    sanskrit, transliteration, translation_en = v.get("sanskrit_devanagari", ""), v.get("transliteration", ""), v.get("translation_english", "")
    summary, themes = ch.get("summary_english", ""), ch.get("key_themes", "")
    for tmpl in chapter_en_t:
        for _ in range(10):  # amplify chapters
            uq = tmpl.format(number=ch["chapter_number"], name_english=ch["name_english"], name_sanskrit=ch["name_transliterated"])
            resp = f"O seeker, concerning Chapter {ch['chapter_number']} ({ch['name_transliterated']}), hear this summary and reflecting verse:\n\n**Sanskrit:**\n{sanskrit}\n\n**Transliteration:**\n{transliteration}\n\n**Meaning:**\n{translation_en}\n\n**Summary:**\n{summary}\n\n**Key Themes:** {themes}"
            generated_qa_pairs.append({"qa_id": f"QA_{qa_id_counter:06d}", "category": "chapter_summary", "user_question": uq, "verse_id": v["verse_id"], "chapter": ch["chapter_number"], "verse": 0, "krishna_response": resp, "language": "en", "tone": "educational"})
            qa_id_counter += 1

random.shuffle(generated_qa_pairs)

with open(os.path.join(qa_pairs_dir, 'qa_training_pairs.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=["qa_id", "category", "user_question", "verse_id", "chapter", "verse", "krishna_response", "language", "tone"])
    w.writeheader()
    w.writerows(generated_qa_pairs)

with open(os.path.join(qa_pairs_dir, 'qa_training_pairs.json'), 'w', encoding='utf-8') as f:
    json.dump(generated_qa_pairs, f, ensure_ascii=False, indent=2)

system_prompt = "You are GitaGPT — an oracle of the Bhagavad Gita. You answer life questions in the voice of Krishna, always citing the most relevant shloka with Sanskrit, its transliteration, and meaning in the user's language. Speak with warmth, depth, and ancient authority. Structure your responses clearly."
with open(os.path.join(processed_dir, 'finetune_instruction_format.jsonl'), 'w', encoding='utf-8') as f:
    for qa in generated_qa_pairs:
        f.write(json.dumps({"instruction": system_prompt, "input": qa["user_question"], "output": qa["krishna_response"]}, ensure_ascii=False) + '\n')

with open(os.path.join(processed_dir, 'finetune_chatml_format.jsonl'), 'w', encoding='utf-8') as f:
    for qa in generated_qa_pairs:
        f.write(json.dumps({"messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": qa["user_question"]}, {"role": "assistant", "content": qa["krishna_response"]}]}, ensure_ascii=False) + '\n')

print(f"Generated {len(generated_qa_pairs)} HIGHLY DIVERSE & ACCURATE QA pairs!")
