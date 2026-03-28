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

with open(os.path.join(raw_dir, "key_verses.json"), 'r', encoding='utf-8') as f:
    key_verses = json.load(f)

# Create a lookup for verses
verse_lookup = {v["verse_id"]: v for v in key_verses}

with open(os.path.join(processed_dir, "problem_verse_mapping.json"), 'r', encoding='utf-8') as f:
    problems = json.load(f)

with open(os.path.join(raw_dir, "concept_glossary.json"), 'r', encoding='utf-8') as f:
    concepts = json.load(f)

english_templates = [
    "I am struggling with {}. What does the Gita say?",
    "How can I overcome {}?",
    "My mind is constantly troubled by {}. Any guidance?",
    "I feel overwhelmed by {}. Please help me.",
    "What is the spiritual perspective on {}?",
    "How do I deal with {} in my daily life?",
    "I am facing {}. What should I do?",
    "Can you give me strength to handle {}?",
    "Why do I suffer from {}?",
    "I need advice on {}.",
    "Krishna, I am lost in {}. Guide me.",
    "What is the deepest root of {} according to the Bhagavad Gita?",
    "Is there a shloka that can help me with {}?",
    "I feel paralyzed by {}. How do I move forward?",
    "Teach me how to conquer {}.",
    "My heart is heavy because of {}. What is the solution?",
    "How would a yogi deal with {}?",
    "I am searching for peace amidst {}.",
    "What is the divine answer to {}?",
    "Can the teachings of Kurukshetra apply to {}?",
    "I am bound by {}. How do I break free?",
    "Tell me a painful truth about {}.",
    "How do I find dharma when surrounded by {}?",
    "My entire life feels ruined by {}. Show me the way.",
    "Is {} an illusion or reality?",
    "My friend is dealing with {}. What advice from the Gita can I share?",
    "How does modern society fix {}?",
    "What is the philosophical meaning behind {}?",
    "Why did Krishna teach about {}?",
    "Can chanting or meditation cure {}?",
    "Give me a quote from the Gita about {}.",
    "Which chapter of the Bhagavad Gita discusses {}?",
    "What is the ultimate cure for {}?",
    "How did Arjuna deal with {}?",
    "I want to eliminate {} from my mind forever.",
    "Is {} a result of my past karma?",
    "How do the three gunas affect {}?",
    "What is the relationship between ego and {}?",
    "Can surrender to God resolve {}?",
    "Provide ancient wisdom for managing {}."
]

hindi_templates = [
    "मैं {} से जूझ रहा हूँ। गीता इस बारे में क्या कहती है?",
    "मैं {} पर कैसे विजय प्राप्त करूँ?",
    "मेरा मन {} से बहुत परेशान है। कोई मार्गदर्शन दें?",
    "मैं {} से अभिभूत महसूस कर रहा हूँ। कृपया मेरी मदद करें।",
    "{} पर आध्यात्मिक दृष्टिकोण क्या है?",
    "मैं अपने दैनिक जीवन में {} से कैसे निपटूँ?",
    "मुझे {} का सामना करना पड़ रहा है। मुझे क्या करना चाहिए?",
    "क्या आप मुझे {} को संभालने की शक्ति दे सकते हैं?",
    "मैं {} से क्यों पीड़ित हूँ?",
    "मुझे {} पर सलाह चाहिए।",
    "हे कृष्ण, मैं {} में खो गया हूँ। मुझे मार्ग दिखाएं।",
    "भगवद गीता के अनुसार {} का मूल कारण क्या है?",
    "क्या कोई श्लोक है जो {} में मेरी मदद कर सके?",
    "मैं {} के कारण असहाय महसूस कर रहा हूँ। मैं आगे कैसे बढ़ूं?",
    "मुझे सिखाएं कि {} पर कैसे विजय प्राप्त करें।",
    "{} के कारण मेरा हृदय भारी है। समाधान क्या है?",
    "एक योगी {} का सामना कैसे करेगा?",
    "मैं {} के बीच शांति की तलाश कर रहा हूँ।",
    "{} का ईश्वरीय उत्तर क्या है?",
    "कुरुक्षेत्र की शिक्षाएं {} पर कैसे लागू हो सकती हैं?",
    "मैं {} से बंधा हूँ। मैं कैसे मुक्त होऊं?",
    "मुझे {} के बारे में एक कड़वा सच बताएं।",
    "जब मैं {} से घिरा हुआ हूँ तो मैं धर्म कैसे खोजूं?",
    "मेरा पूरा जीवन {} से बर्बाद हो गया है। मुझे रास्ता दिखाएं।",
    "क्या {} एक भ्रम है या हकीकत?"
]

concept_en_templates = [
    "What is the meaning of {}?",
    "Can you explain the concept of {} in the Bhagavad Gita?",
    "How do I practice {}?",
    "What does Krishna say about {}?",
    "I want to understand {}. Please guide me."
]
concept_hi_templates = [
    "{} का क्या अर्थ है?",
    "क्या आप भगवद गीता में {} की अवधारणा को समझा सकते हैं?",
    "मैं {} का अभ्यास कैसे करूँ?",
    "कृष्ण {} के बारे में क्या कहते हैं?",
    "मैं {} को समझना चाहता हूँ। कृपया मेरा मार्गदर्शन करें।"
]

wisdom_prefixes = [
    "",
    "As I told Arjuna on the battlefield of Kurukshetra:\n\n",
    "Hear this ancient wisdom, O seeker:\n\n",
    "The divine truth of the matter is this:\n\n",
    "Let your mind find peace in this teaching:\n\n"
]

generated_qa_pairs = []
qa_id_counter = 1

# 1. PROCESS PROBLEMS
for p in problems:
    primary_verse_id = p["primary_verse"]
    if primary_verse_id not in verse_lookup: continue
    v = verse_lookup[primary_verse_id]
    
    keywords = [k.strip() for k in p["problem_keywords"].split(",")]
    
    sanskrit = v.get("sanskrit_devanagari", "")
    transliteration = v.get("transliteration", "")
    translation_en = v.get("translation_english", "")
    translation_hi = v.get("translation_hindi", "")
    purport = v.get("purport_summary", "")
    
    if not (sanskrit and transliteration and translation_en):
        continue
        
    for keyword in keywords:
        if not keyword: continue
        
        # English
        for template in english_templates:
            user_question = template.format(keyword)
            prefix = random.choice(wisdom_prefixes)
            response = f"O seeker, hear this eternal truth:\n\n**Sanskrit:**\n{sanskrit}\n\n**Transliteration:**\n{transliteration}\n\n**Meaning:**\n{translation_en}\n\n{prefix}{purport}"
            generated_qa_pairs.append({
                "qa_id": f"QA_{qa_id_counter:05d}",
                "category": p.get("problem_category", "general"),
                "user_question": user_question,
                "verse_id": v["verse_id"],
                "chapter": v["chapter"],
                "verse": v["verse"],
                "krishna_response": response,
                "language": "en",
                "tone": "compassionate, direct"
            })
            qa_id_counter += 1
            
        # Hindi
        for template in hindi_templates:
            user_question = template.format(keyword)
            response_hi = f"हे साधक, इस शाश्वत सत्य को सुनो:\n\n**Sanskrit:**\n{sanskrit}\n\n**Transliteration:**\n{transliteration}\n\n**Meaning:**\n{translation_hi}\n\n{purport}"
            generated_qa_pairs.append({
                "qa_id": f"QA_{qa_id_counter:05d}",
                "category": p.get("problem_category", "general"),
                "user_question": user_question,
                "verse_id": v["verse_id"],
                "chapter": v["chapter"],
                "verse": v["verse"],
                "krishna_response": response_hi,
                "language": "hi",
                "tone": "compassionate, direct"
            })
            qa_id_counter += 1

# 2. PROCESS CONCEPTS
for c in concepts:
    verse_id = c.get("key_verse")
    # If key verse doesn't exist, we fallback to BG_2_47 as a robust default
    if verse_id not in verse_lookup: verse_id = "BG_2_47"
    v = verse_lookup[verse_id]
    
    sanskrit = v.get("sanskrit_devanagari", "")
    transliteration = v.get("transliteration", "")
    translation_en = v.get("translation_english", "")
    translation_hi = v.get("translation_hindi", "")
    
    term = c.get("term_sanskrit", "")
    meaning_en = c.get("extended_meaning", "")
    
    # English
    for template in concept_en_templates:
        user_question = template.format(term)
        response = f"O seeker, hear this eternal truth:\n\n**Sanskrit:**\n{sanskrit}\n\n**Transliteration:**\n{transliteration}\n\n**Meaning:**\n{translation_en}\n\nTo understand {term}, know this: {meaning_en}"
        generated_qa_pairs.append({
            "qa_id": f"QA_{qa_id_counter:05d}",
            "category": "philosophy",
            "user_question": user_question,
            "verse_id": v["verse_id"],
            "chapter": v["chapter"],
            "verse": v["verse"],
            "krishna_response": response,
            "language": "en",
            "tone": "philosophical"
        })
        qa_id_counter += 1
        
    for template in concept_hi_templates:
        user_question = template.format(term)
        response_hi = f"हे साधक, इस शाश्वत सत्य को सुनो:\n\n**Sanskrit:**\n{sanskrit}\n\n**Transliteration:**\n{transliteration}\n\n**Meaning:**\n{translation_hi}\n\n{term} का अर्थ है: {c.get('primary_meaning', '')}. {meaning_en}"
        generated_qa_pairs.append({
            "qa_id": f"QA_{qa_id_counter:05d}",
            "category": "philosophy",
            "user_question": user_question,
            "verse_id": v["verse_id"],
            "chapter": v["chapter"],
            "verse": v["verse"],
            "krishna_response": response_hi,
            "language": "hi",
            "tone": "philosophical"
        })
        qa_id_counter += 1

random.seed(42)
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
        record = {"instruction": system_prompt, "input": qa["user_question"], "output": qa["krishna_response"]}
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

with open(os.path.join(processed_dir, 'finetune_chatml_format.jsonl'), 'w', encoding='utf-8') as f:
    for qa in generated_qa_pairs:
        record = {"messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": qa["user_question"]}, {"role": "assistant", "content": qa["krishna_response"]}]}
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

print(f"Generated {len(generated_qa_pairs)} highly accurate QA pairs!")
