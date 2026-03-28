# 📥 Data Sources — GitaGPT Dataset

Complete list of every external source you need to download to build the full GitaGPT training corpus. All sources listed here are either public domain, CC-licensed, or freely accessible for research use.

---

## 🔴 Priority 1: Core Text — Bhagavad Gita Full Corpus

These are the foundational texts. Download all of them and cross-reference for accuracy.

---

### 1. Kaggle — Bhagavad Gita Verses (CSV, ready to use)
**URL**: https://www.kaggle.com/datasets/rtatman/bhagavad-gita-verses
**Format**: CSV
**License**: CC BY-SA 4.0
**Contains**: All 700 verses in English, chapter metadata
**How to download**:
```bash
kaggle datasets download -d rtatman/bhagavad-gita-verses
unzip bhagavad-gita-verses.zip -d data/external/kaggle_gita/
```
**Why use it**: Clean, structured CSV — easiest starting point for the verse corpus.

---

### 2. Hugging Face — Bhagavad Gita Dataset
**URL**: https://huggingface.co/datasets/ShubhAgarwal/bhagavad-gita
**Format**: Parquet / CSV via HF datasets API
**License**: CC BY
**Contains**: Verses with multiple translations
**How to download**:
```python
from datasets import load_dataset
ds = load_dataset("ShubhAgarwal/bhagavad-gita")
ds['train'].to_csv('data/external/hf_gita.csv')
```

---

### 3. Sacred Texts Archive — Full Bhagavad Gita (Public Domain)
**URL**: https://www.sacred-texts.com/hin/gita/index.htm
**Format**: HTML pages (need scraping)
**License**: Public Domain
**Contains**: Full text with multiple translations side by side
**How to use**:
```python
import requests
from bs4 import BeautifulSoup

# Fetch each chapter
for ch in range(1, 19):
    url = f"https://www.sacred-texts.com/hin/gita/gita{ch:02d}.htm"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract verse text from <p> tags
    # ... (parse and save to data/external/sacred_texts/)
```

---

### 4. Wikisource Sanskrit — Original Devanagari Text
**URL**: https://sa.wikisource.org/wiki/श्रीमद्भगवद्गीता
**Format**: Wiki markup (parseable)
**License**: CC BY-SA
**Contains**: Original Sanskrit in Devanagari, chapter by chapter
**Direct chapter links**:
```
Chapter 1:  https://sa.wikisource.org/wiki/श्रीमद्भगवद्गीता/प्रथमोऽध्यायः
Chapter 2:  https://sa.wikisource.org/wiki/श्रीमद्भगवद्गीता/द्वितीयोऽध्यायः
...
Chapter 18: https://sa.wikisource.org/wiki/श्रीमद्भगवद्गीता/अष्टादशोऽध्यायः
```

---

### 5. GRETIL — Göttingen Register of Electronic Texts in Indian Languages
**URL**: http://gretil.sub.uni-goettingen.de/gretil/1_sanskr/6_sastra/3_phil/vedanta/bhgsbh_u.htm
**Format**: Plain text (IAST encoding)
**License**: Academic use
**Contains**: Critical edition Sanskrit text in IAST (International Alphabet of Sanskrit Transliteration)
**Note**: This is the most philologically accurate source. Use for Sanskrit validation.

---

### 6. Hindi Wikisource — Hindi Translation
**URL**: https://hi.wikisource.org/wiki/श्रीमद्भगवद्गीता
**Format**: Wiki markup
**License**: CC BY-SA
**Contains**: Full Bhagavad Gita in Hindi translation
**Use for**: Building Hindi training pairs and multilingual data

---

## 🟡 Priority 2: Commentaries & Purports

### 7. Swami Sivananda Commentary (Free PDF)
**URL**: https://www.dlshq.org/download/gitabook.pdf
**Format**: PDF (~400 pages)
**License**: Free distribution permitted
**Contains**: Verse-by-verse English commentary, traditional Vedantic perspective
**How to extract**:
```bash
pip install PyMuPDF
python3 -c "
import fitz
doc = fitz.open('gitabook.pdf')
text = ''
for page in doc:
    text += page.get_text()
with open('data/external/sivananda_commentary.txt', 'w') as f:
    f.write(text)
"
```

---

### 8. Vedabase — Prabhupada's Bhagavad Gita As It Is
**URL**: https://vedabase.io/en/library/bg/
**Format**: Web (HTML)
**License**: Check BBT usage terms; free for personal/educational use
**Contains**: Verse, translation, and detailed purports (commentaries)
**Note**: The purports are extremely detailed — 1–3 paragraphs per verse, 700+ purports total. Ideal for long-form training data.
**How to access**: Browse by chapter at https://vedabase.io/en/library/bg/1/ (Chapter 1), etc.

---

### 9. Gita Press — Authoritative Hindi Commentary
**URL**: https://www.gitapress.org/book/1531
**Format**: Physical book / some digital versions on Archive.org
**License**: Available for religious distribution
**Contains**: Srimad Bhagavad Gita with word-for-word Sanskrit and Hindi commentary
**Archive.org search**: https://archive.org/search?query=gita+press+bhagavad+gita
**Note**: Gita Press (Gorakhpur) is the most authoritative Hindi Gita publisher. Their word meanings are extremely precise.

---

### 10. S. Radhakrishnan Translation — Academic Standard
**URL**: https://archive.org/details/bhagavadgitawith00radh
**Format**: PDF on Archive.org
**License**: Public Domain (1948)
**Contains**: Sanskrit text + detailed academic English translation + commentary
**Download directly**: `wget "https://archive.org/download/bhagavadgitawith00radh/bhagavadgitawith00radh.pdf"`

---

### 11. Tilak's Gita Rahasya (Hindi)
**URL**: https://archive.org/details/GitaRahasya
**Format**: PDF
**License**: Public Domain
**Contains**: Bal Gangadhar Tilak's famous Karma Yoga interpretation of the Gita — essential for the Karma Yoga training data

---

## 🟢 Priority 3: Extended Corpus (Vedantic Context)

### 12. The Principal Upanishads — Radhakrishnan Translation
**URL**: https://archive.org/details/PrincipalUpanishads
**Format**: PDF
**License**: Public Domain
**Contains**: 12 major Upanishads (Brihadaranyaka, Chandogya, Kena, Katha, etc.) — the philosophical foundation of Gita teachings

---

### 13. Yoga Sutras of Patanjali
**URL**: https://www.sacred-texts.com/hin/yogasutr.htm
**Format**: HTML
**License**: Public Domain
**Contains**: 196 sutras on yoga and meditation — directly supplements Gita Chapter 6 (Dhyana Yoga)

---

### 14. Narada Bhakti Sutras
**URL**: https://www.sacred-texts.com/hin/narada/index.htm
**Format**: HTML
**License**: Public Domain
**Contains**: 84 sutras on devotional love — directly supplements Gita Chapter 12 (Bhakti Yoga)

---

### 15. Vivekachudamani — Adi Shankaracharya
**URL**: https://www.sacred-texts.com/hin/sbe08/index.htm
**Format**: HTML
**License**: Public Domain
**Contains**: 580 verses on Advaita Vedanta — enriches Jnana Yoga and self-knowledge sections

---

## 🔵 Priority 4: NLP Tools & Models

### 16. Indic NLP Library
**URL**: https://github.com/anoopkunchukuttan/indic_nlp_library
**Install**: `pip install indic-nlp-library`
**Use for**: Hindi tokenization, normalization, script conversion

---

### 17. AI4Bharat IndicBERT
**URL**: https://huggingface.co/ai4bharat/indic-bert
**Install**: `pip install transformers`
**Use for**: Hindi/Sanskrit embeddings, semantic search in Indian languages
```python
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained('ai4bharat/indic-bert')
model = AutoModel.from_pretrained('ai4bharat/indic-bert')
```

---

### 18. Sanskrit Heritage Segmenter
**URL**: https://sanskrit.inria.fr/
**Type**: Online API + downloadable tool
**Use for**: Sanskrit morphological analysis, word-splitting (sandhi), POS tagging

---

### 19. SanskritNLP Tools
**URL**: https://github.com/sanskrit-coders
**Repos**:
- `indic_transliteration` — Convert between Devanagari, IAST, Harvard-Kyoto
- `sanskrit_parser` — Parse Sanskrit sentences
**Install**: `pip install indic_transliteration`
```python
from indic_transliteration import sanscript
# Convert Devanagari to IAST
iast = sanscript.transliterate("कर्मण्येवाधिकारस्ते", sanscript.DEVANAGARI, sanscript.IAST)
```

---

### 20. Multilingual Sentence Transformer (for RAG)
**URL**: https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
**Install**: `pip install sentence-transformers`
**Use for**: Embedding user questions in English/Hindi for semantic verse retrieval
**Supports**: 50+ languages including Hindi and Sanskrit-adjacent text

---

## 📊 Existing Kaggle Datasets to Reference

| Dataset | URL | Notes |
|---|---|---|
| Bhagavad Gita Verses | https://www.kaggle.com/datasets/rtatman/bhagavad-gita-verses | Best starting CSV |
| Sanskrit Texts Corpus | https://www.kaggle.com/datasets/shubham0204/sanskrit-texts-corpus | Broader Sanskrit |
| Mahabharata Text | https://www.kaggle.com/datasets/daisypath/mahabharata | Context for Gita narrative |
| Hindu Scriptures Dataset | https://www.kaggle.com/datasets/truthfulonion/hindu-scriptures-dataset | Combined scriptures |

---

## 🗂️ Recommended Download Order

```
Priority 1 (Do First):
1. Kaggle Bhagavad Gita CSV          → Immediate verse corpus
2. HuggingFace Gita Dataset          → Additional translations
3. Hindi Wikisource                  → Hindi text

Priority 2 (This Week):
4. Sivananda Commentary PDF          → Training commentary data
5. Vedabase (Prabhupada purports)    → Deep verse explanations
6. Archive.org Radhakrishnan         → Academic translations

Priority 3 (For v2.0):
7. Upanishads corpus                 → Extended Vedantic context
8. Sanskrit NLP tools                → Morphological analysis
9. IndicBERT model                   → Hindi embeddings
```

---

## ⚠️ Usage Notes

1. **Always verify licensing** before using any source commercially. Most listed here are public domain or CC-licensed.
2. **Prabhupada's purports** (Vedabase) are copyrighted by the BBT (Bhaktivedanta Book Trust). Use for research; check terms before commercial deployment.
3. **Gita Press content** is published for religious distribution — confirm terms before use in a commercial AI product.
4. **Academic translations** (Radhakrishnan, Zaehner) published before 1927 are public domain in the US.
5. **Never serve someone else's translation verbatim** in a commercial product without a license. Fine-tune on it, extract structure from it, paraphrase — but don't reproduce wholesale.

---

*For dataset contributions or corrections, open a pull request on the GitaGPT GitHub repository.*
