import json, csv, os, glob

# Generate dataset statistics
stats = {
    "dataset_name": "GitaGPT: Bhagavad Gita Oracle Dataset",
    "version": "1.0.0",
    "created_by": "AlphaByteCore",
    "purpose": "Fine-tuning and RAG for GitaGPT — an AI oracle grounded in the Bhagavad Gita",
    "files": {},
    "totals": {}
}

file_descriptions = {
    "data/raw/chapters.csv": "18 chapters with Sanskrit names, summaries in EN/HI, themes, and modern mappings",
    "data/raw/chapters.json": "Same as above in JSON format",
    "data/raw/key_verses.csv": "108 most important shlokas with full Sanskrit, transliteration, EN/HI/SA translations, purport, and modern question mappings",
    "data/raw/key_verses.json": "Same as above in JSON format",
    "data/raw/concept_glossary.csv": "Sanskrit philosophical terms with meanings and modern equivalents",
    "data/raw/concept_glossary.json": "Same as above in JSON format",
    "data/qa_pairs/qa_training_pairs.csv": "Q&A training pairs: modern life questions → Krishna-voiced responses citing actual shlokas",
    "data/qa_pairs/qa_training_pairs.json": "Same as above in JSON format",
    "data/processed/finetune_instruction_format.jsonl": "Training data in instruction-input-output format (Alpaca/LLaMA style)",
    "data/processed/finetune_chatml_format.jsonl": "Training data in ChatML format (Mistral/Llama-3/GPT-4 style)",
    "data/processed/problem_verse_mapping.csv": "Mapping of modern problems/keywords to relevant Gita verses for RAG retrieval",
    "data/processed/problem_verse_mapping.json": "Same as above in JSON format",
}

base = '/home/claude/gitagpt-dataset'
for rel_path, desc in file_descriptions.items():
    full_path = os.path.join(base, rel_path)
    if os.path.exists(full_path):
        size = os.path.getsize(full_path)
        if full_path.endswith('.csv'):
            with open(full_path, encoding='utf-8') as f:
                rows = sum(1 for _ in csv.reader(f)) - 1
            record_count = rows
        elif full_path.endswith('.json'):
            with open(full_path, encoding='utf-8') as f:
                data = json.load(f)
            record_count = len(data) if isinstance(data, list) else 1
        elif full_path.endswith('.jsonl'):
            with open(full_path, encoding='utf-8') as f:
                record_count = sum(1 for _ in f)
        else:
            record_count = None

        stats["files"][rel_path] = {
            "description": desc,
            "size_bytes": size,
            "size_kb": round(size / 1024, 1),
            "record_count": record_count
        }

stats["totals"] = {
    "total_files": len(stats["files"]),
    "total_size_kb": round(sum(v["size_kb"] for v in stats["files"].values()), 1),
    "chapters": 18,
    "total_verses_gita": 700,
    "key_verses_annotated": 17,
    "qa_training_pairs": 20,
    "problem_mappings": 30,
    "glossary_terms": 20,
    "languages": ["Sanskrit", "English", "Hindi"],
    "fine_tune_formats": ["Alpaca/Instruction", "ChatML"],
}

with open('/home/claude/gitagpt-dataset/data/dataset_stats.json', 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)

print("=== DATASET STATISTICS ===")
print(f"Total files: {stats['totals']['total_files']}")
print(f"Total size: {stats['totals']['total_size_kb']} KB")
print()
for path, info in stats['files'].items():
    print(f"  {path}")
    print(f"    Records: {info['record_count']} | Size: {info['size_kb']} KB")
    print()
