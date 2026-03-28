# 🧠 GitaGPT Fine-Tuning Guide

Complete walkthrough for fine-tuning a Small Language Model (SLM) on the GitaGPT dataset to create your own Bhagavad Gita oracle.

---

## Overview

**Goal**: Fine-tune a 2–8B parameter model so it:
1. Understands that it is the GitaGPT oracle
2. Cites real Gita shlokas (not hallucinated ones)
3. Responds in Krishna's voice — warm, authoritative, grounded in scripture
4. Supports English and Hindi input/output
5. Maps modern questions to the most relevant verse

**Recommended approach**: RAG + Fine-tuning hybrid (best quality)
**Minimal approach**: Fine-tuning only (for resource-constrained deployments)

---

## Step 1: Environment Setup

```bash
# Create environment
conda create -n gitagpt python=3.10
conda activate gitagpt

# Install training dependencies
pip install transformers==4.40.0
pip install trl==0.8.6
pip install peft==0.10.0
pip install bitsandbytes==0.43.0
pip install accelerate==0.29.0
pip install datasets==2.18.0
pip install sentence-transformers==2.7.0
pip install wandb  # optional, for tracking

# For Hindi/Sanskrit tokenization
pip install indic-nlp-library
pip install pydevanagari
```

---

## Step 2: Download Base Model

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Recommended: Phi-3 Mini (fastest, mobile-friendly)
model_name = "microsoft/Phi-3-mini-4k-instruct"

# Alternative: Mistral 7B (better multilingual)
# model_name = "mistralai/Mistral-7B-Instruct-v0.2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto",
    load_in_4bit=True  # QLoRA for memory efficiency
)
```

---

## Step 3: Load and Prepare Training Data

```python
import json
from datasets import Dataset

# Load ChatML format (recommended)
records = []
with open('data/processed/finetune_chatml_format.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        records.append(json.loads(line))

# Format for training
def format_chatml(record):
    messages = record['messages']
    text = ""
    for msg in messages:
        if msg['role'] == 'system':
            text += f"<|system|>\n{msg['content']}<|end|>\n"
        elif msg['role'] == 'user':
            text += f"<|user|>\n{msg['content']}<|end|>\n"
        elif msg['role'] == 'assistant':
            text += f"<|assistant|>\n{msg['content']}<|end|>\n"
    return {"text": text}

dataset = Dataset.from_list([format_chatml(r) for r in records])
dataset = dataset.train_test_split(test_size=0.1, seed=42)
print(f"Train: {len(dataset['train'])} | Test: {len(dataset['test'])}")
```

---

## Step 4: Configure QLoRA (Parameter-Efficient Fine-tuning)

```python
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import TrainingArguments
from trl import SFTTrainer

# Prepare model for QLoRA
model = prepare_model_for_kbit_training(model)

# LoRA configuration
lora_config = LoraConfig(
    r=16,                    # Rank
    lora_alpha=32,           # Scaling factor
    target_modules=[         # Which layers to train
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Expected: ~0.5-2% of total parameters trained
```

---

## Step 5: Training Arguments

```python
training_args = TrainingArguments(
    output_dir="./gitagpt-model",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    optim="paged_adamw_32bit",
    save_steps=50,
    logging_steps=10,
    learning_rate=2e-4,
    weight_decay=0.001,
    fp16=True,
    bf16=False,
    max_grad_norm=0.3,
    max_steps=-1,
    warmup_ratio=0.03,
    group_by_length=True,
    lr_scheduler_type="cosine",
    report_to="wandb",       # Remove if not using wandb
    run_name="gitagpt-v1"
)
```

---

## Step 6: Train

```python
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    peft_config=lora_config,
    dataset_text_field="text",
    max_seq_length=2048,
    tokenizer=tokenizer,
    args=training_args,
    packing=False,
)

trainer.train()
trainer.save_model("./gitagpt-model-final")
```

---

## Step 7: Build the RAG Retrieval Layer

For production quality, combine fine-tuning with verse retrieval:

```python
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import torch

# Load verse database
verses_df = pd.read_csv('data/raw/key_verses.csv')
problems_df = pd.read_csv('data/processed/problem_verse_mapping.csv')

# Build embedding index
embed_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
# This model supports English + Hindi

# Create retrieval corpus: combine all textual fields
corpus = []
for _, row in verses_df.iterrows():
    text = f"{row['modern_question_mapping']} {row['purport_summary']} {row['translation_english']}"
    corpus.append(text)

corpus_embeddings = embed_model.encode(corpus, convert_to_tensor=True)

def retrieve_verse(question: str, top_k: int = 1):
    """Retrieve the most relevant Gita verse for a given question."""
    question_emb = embed_model.encode(question, convert_to_tensor=True)
    scores = util.cos_sim(question_emb, corpus_embeddings)[0]
    top_idx = scores.argmax().item()
    
    verse_row = verses_df.iloc[top_idx]
    return {
        "verse_id": verse_row['verse_id'],
        "chapter": verse_row['chapter'],
        "verse": verse_row['verse'],
        "sanskrit": verse_row['sanskrit_devanagari'],
        "transliteration": verse_row['transliteration'],
        "translation_en": verse_row['translation_english'],
        "translation_hi": verse_row['translation_hindi'],
        "purport": verse_row['purport_summary'],
        "score": scores[top_idx].item()
    }

# Test
result = retrieve_verse("I am afraid of failing my exams")
print(f"Best verse: {result['verse_id']} (score: {result['score']:.3f})")
print(result['sanskrit'])
```

---

## Step 8: RAG + LLM Inference Pipeline

```python
def gitagpt_respond(user_question: str, language: str = "en") -> str:
    """Full GitaGPT pipeline: retrieve verse → generate Krishna response."""
    
    # Step 1: Retrieve best verse
    verse = retrieve_verse(user_question)
    
    # Step 2: Build context-enriched prompt
    verse_context = f"""
Verse: {verse['verse_id']} (Chapter {verse['chapter']}, Verse {verse['verse']})
Sanskrit: {verse['sanskrit']}
Transliteration: {verse['transliteration']}
English Meaning: {verse['translation_en']}
Hindi Meaning: {verse['translation_hi']}
Philosophical Context: {verse['purport']}
"""

    system_prompt = """You are GitaGPT — the Bhagavad Gita Oracle. You speak in the voice of Krishna, 
responding to the modern seeker with wisdom from the Gita. 
Always cite the provided verse in your response with Sanskrit, transliteration, and meaning.
Be warm, authoritative, and personally relevant to their exact situation.
Speak directly to the person, address their specific pain or question."""

    user_prompt = f"""
The seeker asks: "{user_question}"

The most relevant Gita verse for this question:
{verse_context}

Respond as Krishna, citing this verse and applying its wisdom to their specific situation.
Language for response: {"English" if language == "en" else "Hindi"}
"""

    # Step 3: Generate with fine-tuned model
    inputs = tokenizer(f"<|system|>\n{system_prompt}<|end|>\n<|user|>\n{user_prompt}<|end|>\n<|assistant|>\n",
                      return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=600,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.1,
        )
    
    response = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
    return response

# Test
print(gitagpt_respond("I feel paralyzed by fear of failure"))
```

---

## Step 9: Evaluation

```python
# Evaluate verse retrieval accuracy
test_cases = [
    ("I am afraid of dying", "BG_2_20"),
    ("My anger is ruining my life", "BG_2_62"),
    ("I feel my work has no meaning", "BG_3_21"),
    ("I lost someone I loved", "BG_2_14"),
    ("How do I find inner peace", "BG_6_5"),
]

correct = 0
for question, expected_verse_id in test_cases:
    result = retrieve_verse(question)
    if result['verse_id'] == expected_verse_id:
        correct += 1
        print(f"✓ '{question}' → {result['verse_id']}")
    else:
        print(f"✗ '{question}' → got {result['verse_id']}, expected {expected_verse_id}")

print(f"\nRetrieval Accuracy: {correct}/{len(test_cases)} = {correct/len(test_cases)*100:.0f}%")
```

---

## Expanding the Dataset (Roadmap)

To reach production quality, expand from the seed set to:

| Component | Seed (v1.0) | Target (v2.0) |
|---|---|---|
| Annotated verses | 17 | 108 (all major shlokas) |
| Q&A pairs | 20 | 1,000+ |
| Problem mappings | 30 | 100+ |
| Languages | EN, HI | + Urdu, Gujarati, Marathi, Tamil |

**Data augmentation strategy**:
1. Use GPT-4 / Claude to generate diverse question paraphrases for each verse
2. Manually curate and verify responses for philosophical accuracy
3. Add Prabhupada's purports as long-form commentary data
4. Include Upanishad verses for extended Vedantic context

---

## Hardware Requirements

| Setup | GPU | VRAM | Training Time (20 pairs) |
|---|---|---|---|
| Minimum | RTX 3090 | 24 GB | ~30 min |
| Recommended | A100 40GB | 40 GB | ~15 min |
| Cloud (budget) | T4 (Colab) | 16 GB | ~1 hr |
| Production | A100 80GB | 80 GB | ~10 min |

**Free cloud options**:
- Google Colab Pro (~$10/month) — T4/A100 access
- Kaggle Notebooks — Free T4/P100
- Lightning AI — Free tier with GPU
- Vast.ai — Cheap A100 rentals

---

*For questions and contributions, open an issue on the GitHub repository.*
