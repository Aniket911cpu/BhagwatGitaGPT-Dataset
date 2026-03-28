# 📐 Schema Reference — GitaGPT Dataset

Field-by-field documentation for every file in the dataset. Use this when integrating the data into your pipeline.

---

## `data/raw/chapters.csv`

**Purpose**: Chapter-level metadata for all 18 chapters of the Bhagavad Gita.
**Rows**: 18 (one per chapter)
**Encoding**: UTF-8

| Field | Type | Example | Description |
|---|---|---|---|
| `chapter_number` | int | `2` | Chapter number (1–18) |
| `name_transliterated` | string | `"Sankhya Yoga"` | English transliteration of the Sanskrit chapter name |
| `name_sanskrit` | string | `"सांख्य योग"` | Chapter name in Devanagari script |
| `name_english` | string | `"The Yoga of Knowledge"` | Full English translation of chapter name |
| `verse_count` | int | `72` | Number of verses in this chapter |
| `summary_english` | string | `"Krishna begins his teaching..."` | 2–3 sentence English summary of the chapter |
| `summary_hindi` | string | `"कृष्ण आत्मा की अमरता..."` | 2–3 sentence Hindi summary of the chapter |
| `key_themes` | string | `"soul immortality, duty, nishkama karma"` | Comma-separated list of philosophical themes |
| `modern_mapping` | string | `"career anxiety, fear of death"` | Modern life domains this chapter addresses |

**Joining**: Use `chapter_number` to join with `key_verses.csv` on the `chapter` field.

---

## `data/raw/key_verses.csv`

**Purpose**: Fully annotated shlokas — the core of the dataset.
**Rows**: 17 in v1.0, targeting 108 (all major shlokas)
**Encoding**: UTF-8

| Field | Type | Example | Description |
|---|---|---|---|
| `verse_id` | string (PK) | `"BG_2_47"` | Unique verse identifier. Format: `BG_{chapter}_{verse}` |
| `chapter` | int | `2` | Chapter number |
| `verse` | int | `47` | Verse number within the chapter |
| `sanskrit_devanagari` | string | `"कर्मण्येवाधिकारस्ते..."` | Original Sanskrit text in Devanagari script |
| `transliteration` | string | `"karmany evadhikaras te..."` | Roman transliteration using IAST convention |
| `translation_english` | string | `"You have a right to perform..."` | Full English translation (1–4 sentences) |
| `translation_hindi` | string | `"तुम्हारा अधिकार केवल..."` | Full Hindi translation |
| `word_meanings` | string | `"karmani=in action; eva=certainly..."` | Semicolon-separated word-by-word breakdown |
| `purport_summary` | string | `"This is the most famous verse..."` | 3–5 sentence philosophical commentary |
| `modern_question_mapping` | string | `"fear of failure, performance anxiety..."` | Comma-separated modern problems this verse addresses |
| `yoga_category` | string | `"Karma Yoga"` | Which yoga path/school this verse belongs to |
| `difficulty_level` | enum | `"foundational"` | `foundational` / `intermediate` / `advanced` |
| `speaker` | string | `"Krishna"` | Who speaks this verse: Krishna, Arjuna, Sanjaya, or Dhritarashtra |
| `tags` | string | `"karma, duty, detachment, action"` | Comma-separated search tags |

**Primary key**: `verse_id`
**Foreign key**: `chapter` → `chapters.chapter_number`

---

## `data/raw/concept_glossary.csv`

**Purpose**: Sanskrit philosophical terms with meanings and modern equivalents.
**Rows**: 20 in v1.0
**Encoding**: UTF-8

| Field | Type | Example | Description |
|---|---|---|---|
| `term_sanskrit` | string (PK) | `"Dharma"` | Sanskrit term in Roman script |
| `devanagari` | string | `"धर्म"` | Term in Devanagari script |
| `transliteration` | string | `"dharma"` | IAST transliteration (lowercase) |
| `primary_meaning` | string | `"duty, righteousness, cosmic order"` | Short definition (1 line) |
| `extended_meaning` | string | `"The moral law governing..."` | 2–4 sentence philosophical explanation |
| `modern_equivalent` | string | `"purpose, integrity, moral duty"` | How a modern reader might understand this |
| `appears_in_chapters` | string | `"1,2,3,4,11,16,18"` | Comma-separated chapter numbers where this term is central |
| `key_verse` | string | `"BG_4_7"` | Most representative verse for this concept |

**Primary key**: `term_sanskrit`
**Foreign key**: `key_verse` → `key_verses.verse_id`

---

## `data/qa_pairs/qa_training_pairs.csv`

**Purpose**: Human-written Q&A pairs for fine-tuning — the model learns to respond like this.
**Rows**: 20 in v1.0 (seed set)
**Encoding**: UTF-8

| Field | Type | Example | Description |
|---|---|---|---|
| `qa_id` | string (PK) | `"QA_001"` | Unique ID. Format: `QA_{number}` |
| `category` | string | `"anxiety_fear"` | Problem category (see categories below) |
| `user_question` | string | `"I feel paralyzed by fear..."` | The user's question — natural, conversational |
| `verse_id` | string | `"BG_2_47"` | The Gita verse cited in the response |
| `chapter` | int | `2` | Chapter number of the cited verse |
| `verse` | int | `47` | Verse number of the cited verse |
| `krishna_response` | string | `"O seeker, hear this eternal truth..."` | Full response in Krishna's voice with Sanskrit + wisdom |
| `language` | enum | `"en"` | Language of the question and response: `en` or `hi` |
| `tone` | string | `"compassionate, direct"` | Description of the response tone |
| `tags` | string | `"fear, failure, karma yoga"` | Comma-separated tags |

**Primary key**: `qa_id`
**Foreign key**: `verse_id` → `key_verses.verse_id`

**Category values**:
- `anxiety_fear` — Fear of failure, death anxiety, panic, overwhelm
- `grief_loss` — Mourning, depression, suffering, pain
- `career_duty` — Work meaning, career choices, procrastination, burnout
- `relationships` — Betrayal, anger, forgiveness, family conflict, heartbreak
- `mind_peace` — Anger management, inner peace, comparison, addiction
- `purpose_existence` — Life purpose, dharma, feeling lost, free will
- `devotion_faith` — Faith in God, unworthiness, surrender, doubt
- `leadership` — Leadership, team management, injustice, setting example
- `surrender_liberation` — Helplessness, letting go, control, crisis

---

## `data/processed/finetune_instruction_format.jsonl`

**Purpose**: Training-ready data in Alpaca/LLaMA instruction format.
**Format**: JSONL (one JSON object per line)

**Schema per line**:
```json
{
  "instruction": "string — The system instruction (GitaGPT's role)",
  "input": "string — The user's question",
  "output": "string — Krishna's response with shloka",
  "metadata": {
    "verse_id": "string — e.g. BG_2_47",
    "chapter": "int",
    "verse": "int",
    "category": "string",
    "language": "string (en or hi)"
  }
}
```

**Compatible models**: LLaMA, Alpaca, Vicuna, any model using instruction format
**Training library**: Use with `trl.SFTTrainer` or `axolotl`

---

## `data/processed/finetune_chatml_format.jsonl`

**Purpose**: Training-ready data in ChatML / OpenAI messages format.
**Format**: JSONL (one JSON object per line)

**Schema per line**:
```json
{
  "messages": [
    {
      "role": "system",
      "content": "string — GitaGPT system prompt"
    },
    {
      "role": "user",
      "content": "string — The user's question"
    },
    {
      "role": "assistant",
      "content": "string — Krishna's full response"
    }
  ]
}
```

**Compatible models**: Mistral, LLaMA-3, Phi-3, GPT-4 (fine-tune API), Gemma
**Training library**: Use with `trl.SFTTrainer` with `tokenizer.apply_chat_template()`

---

## `data/processed/problem_verse_mapping.csv`

**Purpose**: Keyword-to-verse retrieval index for RAG systems.
**Rows**: 30 in v1.0
**Encoding**: UTF-8

| Field | Type | Example | Description |
|---|---|---|---|
| `problem_id` | string (PK) | `"P001"` | Unique problem ID |
| `problem_category` | string | `"anxiety"` | Broad category |
| `problem_keywords` | string | `"anxiety, anxious, worry, overthinking"` | Comma-separated keywords for BM25 / keyword matching |
| `problem_description` | string | `"General anxiety and excessive worrying"` | Human-readable description |
| `primary_verse` | string | `"BG_6_35"` | Best verse for this problem |
| `secondary_verses` | string | `"BG_2_47,BG_2_14"` | Comma-separated alternative verses |
| `yoga_path` | string | `"Dhyana Yoga"` | Which yoga path addresses this |
| `chapter_focus` | int | `6` | Primary chapter to reference |

**Primary key**: `problem_id`
**Foreign keys**: `primary_verse`, `secondary_verses` → `key_verses.verse_id`

**Use in RAG pipeline**:
```python
# BM25 keyword matching
from rank_bm25 import BM25Okapi
import pandas as pd

df = pd.read_csv('data/processed/problem_verse_mapping.csv')
corpus = [row['problem_keywords'].split(', ') for _, row in df.iterrows()]
bm25 = BM25Okapi(corpus)

query = "I am afraid of dying"
scores = bm25.get_scores(query.lower().split())
best_idx = scores.argmax()
print(df.iloc[best_idx]['primary_verse'])  # → BG_2_20
```

---

## `data/dataset_stats.json`

**Purpose**: Auto-generated metadata and statistics for the dataset.

```json
{
  "dataset_name": "string",
  "version": "string",
  "created_by": "string",
  "purpose": "string",
  "files": {
    "relative/path/to/file": {
      "description": "string",
      "size_bytes": "int",
      "size_kb": "float",
      "record_count": "int"
    }
  },
  "totals": {
    "total_files": "int",
    "total_size_kb": "float",
    "chapters": 18,
    "total_verses_gita": 700,
    "key_verses_annotated": "int",
    "qa_training_pairs": "int",
    "problem_mappings": "int",
    "glossary_terms": "int",
    "languages": ["Sanskrit", "English", "Hindi"],
    "fine_tune_formats": ["Alpaca/Instruction", "ChatML"]
  }
}
```

---

## Relationships Between Files

```
chapters.csv
    └── chapter_number
            └── (FK) key_verses.chapter
                        └── verse_id (PK)
                                ├── (FK) qa_training_pairs.verse_id
                                ├── (FK) problem_verse_mapping.primary_verse
                                └── (FK) concept_glossary.key_verse
```

---

## Encoding Notes

- All files are **UTF-8 encoded**
- Devanagari text (Sanskrit, Hindi) is stored as native Unicode — do not convert to ASCII
- Transliteration uses **IAST** (International Alphabet of Sanskrit Transliteration) convention
- CSV files use standard comma delimiter with double-quote escaping for fields containing commas
- JSONL files contain one complete JSON object per line (no trailing commas, no array wrapper)

---

## Null / Missing Values

| File | Field | Null policy |
|---|---|---|
| `key_verses.csv` | `translation_hindi` | May be empty string in v1.0 — fill from external sources |
| `key_verses.csv` | `word_meanings` | May be partial — Sanskrit NLP tools can extend |
| `qa_training_pairs.csv` | All fields | No nulls — all fields required |
| `problem_verse_mapping.csv` | `secondary_verses` | May be empty string if only one verse is relevant |

---

*Schema version 1.0.0 — Last updated with dataset v1.0.0*
