import json
import os
import random
import csv

# Define paths dynamically based on current script location
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.dirname(script_dir)
raw_data_path = os.path.join(dataset_dir, "data", "raw", "key_verses.json")
processed_dir = os.path.join(dataset_dir, "data", "processed")
qa_pairs_dir = os.path.join(dataset_dir, "data", "qa_pairs")

os.makedirs(processed_dir, exist_ok=True)
os.makedirs(qa_pairs_dir, exist_ok=True)

with open(raw_data_path, 'r', encoding='utf-8') as f:
    key_verses = json.load(f)

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
    "I need advice on {}."
]

hindi_templates = [
    "मैं {} से जूझ रहा हूँ। गीता इस बारे में क्या कहती है?",
    "मैं {} पर कैसे विजय प्राप्त करूँ?",
    "मेरा मन {} से बहुत परेशान है। कोई मार्गदर्शन दें?",
    "मैं {} से अभिभूत महसूस कर रहा हूँ। कृपया मेरी मदद करें।",
    "{} पर आध्यात्मिक दृष्टिकोण क्या है?"
]

generated_qa_pairs = []
qa_id_counter = 1

for verse in key_verses:
    topics = [t.strip() for t in verse.get("modern_question_mapping", "").split(",")]
    sanskrit = verse.get("sanskrit_devanagari", "")
    transliteration = verse.get("transliteration", "")
    translation_en = verse.get("translation_english", "")
    translation_hi = verse.get("translation_hindi", "")
    purport = verse.get("purport_summary", "")
    
    if not (sanskrit and transliteration and translation_en):
        continue
        
    for topic in topics:
        if not topic: continue
        
        # Generate English questions
        for template in english_templates:
            user_question = template.format(topic)
            wisdom = purport
            
            response = f"O seeker, hear this eternal truth:\n\n**Sanskrit:**\n{sanskrit}\n\n**Transliteration:**\n{transliteration}\n\n**Meaning:**\n{translation_en}\n\n{wisdom}"
            
            generated_qa_pairs.append({
                "qa_id": f"QA_{qa_id_counter:04d}",
                "category": verse.get("yoga_category", "general"),
                "user_question": user_question,
                "verse_id": verse["verse_id"],
                "chapter": verse["chapter"],
                "verse": verse["verse"],
                "krishna_response": response,
                "language": "en",
                "tone": "compassionate, direct"
            })
            qa_id_counter += 1
            
        # Generate Hindi questions
        for template in hindi_templates:
            user_question = template.format(topic)
            
            response_hi = f"हे साधक, इस शाश्वत सत्य को सुनो:\n\n**Sanskrit:**\n{sanskrit}\n\n**Transliteration:**\n{transliteration}\n\n**Meaning:**\n{translation_hi}\n\n{wisdom}"
            
            generated_qa_pairs.append({
                "qa_id": f"QA_{qa_id_counter:04d}",
                "category": verse.get("yoga_category", "general"),
                "user_question": user_question,
                "verse_id": verse["verse_id"],
                "chapter": verse["chapter"],
                "verse": verse["verse"],
                "krishna_response": response_hi,
                "language": "hi",
                "tone": "compassionate, direct"
            })
            qa_id_counter += 1

# Shuffle data natively
random.seed(42)
random.shuffle(generated_qa_pairs)

# Save QA Pairs
with open(os.path.join(qa_pairs_dir, 'qa_training_pairs.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=["qa_id", "category", "user_question", "verse_id", "chapter", "verse", "krishna_response", "language", "tone"])
    w.writeheader()
    w.writerows(generated_qa_pairs)

with open(os.path.join(qa_pairs_dir, 'qa_training_pairs.json'), 'w', encoding='utf-8') as f:
    json.dump(generated_qa_pairs, f, ensure_ascii=False, indent=2)

system_prompt = "You are GitaGPT — an oracle of the Bhagavad Gita. You answer life questions in the voice of Krishna, always citing the most relevant shloka with Sanskrit, its transliteration, and meaning in the user's language. Speak with warmth, depth, and ancient authority. Structure your responses clearly."

with open(os.path.join(processed_dir, 'finetune_instruction_format.jsonl'), 'w', encoding='utf-8') as f:
    for qa in generated_qa_pairs:
        record = {
            "instruction": system_prompt,
            "input": qa["user_question"],
            "output": qa["krishna_response"]
        }
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

with open(os.path.join(processed_dir, 'finetune_chatml_format.jsonl'), 'w', encoding='utf-8') as f:
    for qa in generated_qa_pairs:
        record = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": qa["user_question"]},
                {"role": "assistant", "content": qa["krishna_response"]}
            ]
        }
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

print(f"Generated {len(generated_qa_pairs)} QA pairs!")
