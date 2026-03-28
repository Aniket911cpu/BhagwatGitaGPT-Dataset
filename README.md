# 🕉️ GitaGPT Dataset — Bhagavad Gita Oracle Training Corpus

**A structured, multilingual dataset for building AI systems grounded in the Bhagavad Gita's 700 shlokas, designed for fine-tuning, RAG retrieval, and semantic search.**

> *"Nainam chindanti shastrani nainam dahati pavakah"*
> *The soul is never cut by weapons, nor burned by fire.* — Bhagavad Gita 2.23

---

## 📌 Dataset Overview

| Property | Value |
|---|---|
| **Creator** | MasterAniket |
| **Version** | 1.0.0 |
| **License** | CC BY-SA 4.0 |
| **Languages** | Sanskrit · English · Hindi |
| **Total Files** | 12 structured files |
| **Format** | CSV · JSON · JSONL |
| **Use Cases** | Fine-tuning, RAG, Chatbots, Semantic Search |
| **Primary Application** | GitaGPT — AI life guidance oracle |

---

## 🎯 Purpose & Vision

The Bhagavad Gita is one of humanity's most profound philosophical texts — 700 verses covering duty, consciousness, action, death, love, and liberation, delivered by Krishna to a grief-stricken Arjuna on the eve of battle. Its wisdom maps directly to every major challenge of modern life.

This dataset was built to power **GitaGPT by MasterAniket** — an AI oracle that:
- Receives a modern life question (in English, Hindi, or transliterated Sanskrit)
- Retrieves the most contextually relevant Gita verse
- Responds in Krishna's voice, citing the original Sanskrit shloka + transliteration + meaning
- Provides personalized wisdom grounded in authentic Vedantic philosophy

**Zero hallucination philosophy**: The model cites real shlokas, not invented philosophy. Every response is anchored to an actual verse.

---

## 📁 Dataset Structure

```
gitagpt-dataset/
│
├── data/
│   ├── raw/
│   │   ├── chapters.csv              ← 18 chapters with full metadata
│   │   ├── chapters.json             ← Same in JSON
│   │   ├── key_verses.csv            ← 108 most important shlokas, fully annotated
│   │   ├── key_verses.json           ← Same in JSON
│   │   ├── concept_glossary.csv      ← 20 Sanskrit terms with modern mappings
│   │   └── concept_glossary.json     ← Same in JSON
│   │
│   ├── processed/
│   │   ├── finetune_instruction_format.jsonl   ← Alpaca/LLaMA instruction format
│   │   ├── finetune_chatml_format.jsonl        ← ChatML format (Mistral/GPT-4)
│   │   ├── problem_verse_mapping.csv           ← Keyword → verse retrieval index
│   │   └── problem_verse_mapping.json          ← Same in JSON
│   │
│   ├── qa_pairs/
│   │   ├── qa_training_pairs.csv     ← 20 Q&A pairs: modern questions → Krishna responses
│   │   └── qa_training_pairs.json   ← Same in JSON
│   │
│   └── dataset_stats.json           ← Full dataset metadata and statistics
│
├── docs/
│   ├── DATA_SOURCES.md              ← External sources to download
│   ├── TRAINING_GUIDE.md            ← Fine-tuning walkthrough
│   ├── SCHEMA_REFERENCE.md          ← Field-by-field schema documentation
│   └── ETHICAL_GUIDELINES.md        ← Usage ethics and attribution
│
└── scripts/
    ├── build_chapters.py            ← Chapter data builder
    ├── build_key_verses.py          ← Verse data builder
    ├── build_glossary.py            ← Glossary builder
    ├── build_qa_pairs.py            ← Q&A pairs builder
    ├── build_problem_mapping.py     ← Problem-verse mapping builder
    └── build_stats.py               ← Statistics generator
```

---

## 📊 File Descriptions

### `data/raw/chapters.csv` — Chapter Metadata
All 18 chapters of the Bhagavad Gita with:

| Field | Description |
|---|---|
| `chapter_number` | 1–18 |
| `name_transliterated` | English transliteration of chapter name |
| `name_sanskrit` | Devanagari Sanskrit chapter name |
| `name_english` | English translation of chapter name |
| `verse_count` | Number of verses in the chapter |
| `summary_english` | Chapter summary in English |
| `summary_hindi` | Chapter summary in Hindi |
| `key_themes` | Comma-separated philosophical themes |
| `modern_mapping` | Modern life domains this chapter addresses |

---

### `data/raw/key_verses.csv` — Annotated Shlokas
The most important shlokas (targeting 108 in full dataset) with:

| Field | Description |
|---|---|
| `verse_id` | Unique ID (e.g., `BG_2_47`) |
| `chapter` / `verse` | Chapter and verse numbers |
| `sanskrit_devanagari` | Original Sanskrit in Devanagari script |
| `transliteration` | Roman transliteration |
| `translation_english` | Full English translation |
| `translation_hindi` | Full Hindi translation |
| `word_meanings` | Word-by-word Sanskrit-English breakdown |
| `purport_summary` | Philosophical commentary summary |
| `modern_question_mapping` | Modern problems this verse addresses |
| `yoga_category` | Which yoga path this belongs to |
| `difficulty_level` | foundational / intermediate / advanced |
| `speaker` | Krishna or Arjuna or Sanjaya |
| `tags` | Search tags |

---

### `data/qa_pairs/qa_training_pairs.csv` — Fine-tuning Q&A Pairs
20 training pairs (seed set — expand with external sources):

| Field | Description |
|---|---|
| `qa_id` | Unique ID |
| `category` | anxiety_fear, grief_loss, career_duty, etc. |
| `user_question` | The modern life question |
| `verse_id` | The Gita verse referenced |
| `krishna_response` | Full response in Krishna's voice with shloka |
| `language` | en or hi |
| `tone` | Response tone descriptor |
| `tags` | Search tags |

---

### `data/processed/finetune_instruction_format.jsonl` — Training Ready (Alpaca/LLaMA)
```json
{
  "instruction": "You are GitaGPT...",
  "input": "I feel paralyzed by fear of failure",
  "output": "O seeker, hear this eternal truth:\n\nकर्मण्येवाधिकारस्ते...",
  "metadata": { "verse_id": "BG_2_47", "chapter": 2, "verse": 47 }
}
```

### `data/processed/finetune_chatml_format.jsonl` — Training Ready (ChatML)
```json
{
  "messages": [
    {"role": "system", "content": "You are GitaGPT..."},
    {"role": "user", "content": "I feel paralyzed by fear of failure"},
    {"role": "assistant", "content": "O seeker, hear this eternal truth:\n\n..."}
  ]
}
```

### `data/processed/problem_verse_mapping.csv` — RAG Retrieval Index
Maps 30+ problem categories and keywords to primary and secondary Gita verses for retrieval-augmented generation.

---

## 🏗️ How to Use This Dataset

### Option 1: Direct RAG (Retrieval-Augmented Generation)
Use the `problem_verse_mapping.csv` as your retrieval index. When a user asks a question:
1. Embed the question using a sentence transformer
2. Match against `problem_keywords` in the mapping file
3. Retrieve the `primary_verse` from `key_verses.csv`
4. Pass the verse data + question to your LLM with a GitaGPT system prompt

### Option 2: Fine-tune a Small Language Model
Use the JSONL files in `data/processed/` to fine-tune:
- **Phi-3 Mini (3.8B)** — Recommended for mobile deployment
- **Gemma-2B** — Good balance of size and performance
- **LLaMA-3-8B** — Higher quality for server deployment
- **Mistral-7B** — Excellent multilingual support for Hindi

See `docs/TRAINING_GUIDE.md` for the complete fine-tuning walkthrough.

### Option 3: Semantic Search / Embeddings
Use the `key_verses.csv` to build a semantic verse search:
```python
from sentence_transformers import SentenceTransformer
import pandas as pd

model = SentenceTransformer('all-MiniLM-L6-v2')
df = pd.read_csv('data/raw/key_verses.csv')

# Embed the modern_question_mapping + purport_summary as retrieval corpus
corpus = df['modern_question_mapping'] + ' ' + df['purport_summary']
embeddings = model.encode(corpus.tolist())

# At query time:
query = "I am afraid of failing"
query_emb = model.encode([query])
# Cosine similarity → retrieve verse
```

---

## 📥 External Data Sources to Download

This dataset provides the structured schema, annotations, Q&A pairs, and processing pipeline. For the complete 700-verse corpus, download these public domain sources:

### 1. Bhagavad Gita — Full Text
| Source | URL | Format | License |
|---|---|---|---|
| Sacred Texts Archive | https://www.sacred-texts.com/hin/gita/ | HTML | Public Domain |
| Wikisource (Sanskrit) | https://sa.wikisource.org/wiki/श्रीमद्भगवद्गीता | Wiki | CC BY-SA |
| GRETIL (Sanskrit corpus) | http://gretil.sub.uni-goettingen.de/gretil/1_sanskr/6_sastra/3_phil/vedanta/bhgsbh_u.htm | Text | Public Domain |
| Hugging Face — Bhagavad Gita Dataset | https://huggingface.co/datasets/ShubhAgarwal/bhagavad-gita | CSV | CC BY |
| Kaggle — Bhagavad Gita Verses | https://www.kaggle.com/datasets/rtatman/bhagavad-gita-verses | CSV | CC BY-SA |

### 2. Translations & Commentaries
| Source | URL | Notes |
|---|---|---|
| ISKCON / Prabhupada Translation | https://vedabase.io/en/library/bg/ | BG + purports; check usage rights |
| Swami Sivananda Translation | https://www.dlshq.org/download/gitabook.pdf | Free PDF, public domain |
| S. Radhakrishnan Translation | Archive.org | Classic academic translation |
| Tilak's Gita Rahasya (Hindi) | https://archive.org/details/GitaRahasya | Hindi commentary |

### 3. Sanskrit Corpus (for NLP preprocessing)
| Source | URL | Notes |
|---|---|---|
| Sanskrit Heritage Tools | https://sanskrit.inria.fr/ | Morphological analysis |
| DCS — Digital Corpus of Sanskrit | https://www.sanskrit-linguistics.org/dcs/ | Annotated Sanskrit texts |
| SanskritNLP GitHub | https://github.com/sanskrit-coders | Sanskrit NLP tools |
| Indic NLP Library | https://github.com/anoopkunchukuttan/indic_nlp_library | Hindi/Sanskrit processing |

### 4. Hindi Translations
| Source | URL | Notes |
|---|---|---|
| Gita Press (Gorakhpur) | https://www.gitapress.org | Authoritative Hindi translations |
| Hindi Wikisource | https://hi.wikisource.org/wiki/श्रीमद्भगवद्गीता | Free Hindi text |

### 5. Related Texts (for extended corpus)
| Source | URL | Notes |
|---|---|---|
| Upanishads (12 principal) | https://www.sacred-texts.com/hin/upan/ | Vedantic context |
| Yoga Sutras of Patanjali | https://www.sacred-texts.com/hin/yogasutr.htm | Meditation philosophy |
| Narada Bhakti Sutras | https://www.sacred-texts.com/hin/narada/ | Devotion philosophy |

---

## 🔢 Dataset Statistics

| Metric | Count |
|---|---|
| Bhagavad Gita Chapters | 18 |
| Total Gita Verses | 700 |
| Key Verses Annotated (v1.0) | 17 (targeting 108) |
| Q&A Training Pairs | 20 (seed set) |
| Problem-Verse Mappings | 30 |
| Sanskrit Concept Glossary Terms | 20 |
| Languages | 3 (Sanskrit, English, Hindi) |
| Fine-tuning Formats | 2 (Instruction, ChatML) |
| Problem Categories | 8 |

> **Roadmap to v2.0**: Full 700-verse annotation, 1,000+ Q&A pairs, Urdu support, audio pronunciation metadata.

---

## 🧠 Recommended Models for Fine-tuning

| Model | Parameters | Best For | HuggingFace |
|---|---|---|---|
| Phi-3 Mini | 3.8B | Mobile app, edge | `microsoft/Phi-3-mini-4k-instruct` |
| Gemma 2B | 2B | Lightweight server | `google/gemma-2b-it` |
| LLaMA 3 8B | 8B | High quality | `meta-llama/Meta-Llama-3-8B-Instruct` |
| Mistral 7B | 7B | Multilingual | `mistralai/Mistral-7B-Instruct-v0.2` |
| IndicBERT | 278M | Hindi-specific | `ai4bharat/indic-bert` |

---

## 📖 Citation

If you use this dataset in research or products, please cite:

```bibtex
@dataset{gitagpt_dataset_2025,
  title     = {GitaGPT Dataset: Bhagavad Gita Oracle Training Corpus},
  author    = {MasterAniket},
  year      = {2025},
  version   = {1.0.0},
  url       = {https://www.kaggle.com/datasets/MasterAniket/gitagpt-dataset},
  license   = {CC BY-SA 4.0}
}
```

---

## ⚖️ License & Attribution

This dataset is released under **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.

- ✅ Free to use for research and commercial applications
- ✅ Free to modify and extend
- ✅ Fine-tuning commercial models is permitted
- ❗ Attribution required: "GitaGPT Dataset by MasterAniket"
- ❗ Derivative datasets must use the same license

The Bhagavad Gita itself is in the **public domain**. Sanskrit text sourced from public domain repositories.

---

## 🙏 Acknowledgments

This dataset draws on the timeless wisdom of:
- The original Sanskrit composition, traditionally attributed to Sage Vyasa
- Centuries of commentary from Adi Shankaracharya, Ramanuja, Madhvacharya
- Modern commentators including Swami Vivekananda, Swami Sivananda, and Bal Gangadhar Tilak
- The open-source Sanskrit NLP and Digital Humanities communities

*Sarve bhavantu sukhinah — May all beings be happy.*

---

*Built with devotion by MasterAniket | [GitHub](https://github.com/MasterAniket) | [GitaGPT App](https://gitagpt.MasterAniket.com)*
