#!/usr/bin/env python3
"""
GitaGPT Dataset — Master Build Script
Run this to regenerate all dataset files from scratch.
Usage: python3 scripts/build_all.py
"""

import subprocess
import sys
import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SCRIPTS = BASE_DIR / "scripts"

def run(script_name, description):
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"  Script: {script_name}")
    print(f"{'='*60}")
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / script_name)],
        cwd=str(BASE_DIR),
        capture_output=False
    )
    if result.returncode != 0:
        print(f"\n❌ FAILED: {script_name}")
        sys.exit(1)
    print(f"✅ Done: {script_name}")

def check_dirs():
    dirs = [
        "data/raw", "data/processed", "data/qa_pairs",
        "data/multilingual", "docs", "scripts", "sample_outputs"
    ]
    for d in dirs:
        (BASE_DIR / d).mkdir(parents=True, exist_ok=True)
    print("✅ Directory structure verified")

def print_summary():
    stats_path = BASE_DIR / "data" / "dataset_stats.json"
    if stats_path.exists():
        with open(stats_path) as f:
            stats = json.load(f)
        print(f"\n{'='*60}")
        print("  DATASET BUILD COMPLETE")
        print(f"{'='*60}")
        print(f"  Files:       {stats['totals']['total_files']}")
        print(f"  Size:        {stats['totals']['total_size_kb']} KB")
        print(f"  Chapters:    {stats['totals']['chapters']}")
        print(f"  Key Verses:  {stats['totals']['key_verses_annotated']}")
        print(f"  Q&A Pairs:   {stats['totals']['qa_training_pairs']}")
        print(f"  Problem Maps:{stats['totals']['problem_mappings']}")
        print(f"  Languages:   {', '.join(stats['totals']['languages'])}")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    print("\n🕉️  GitaGPT Dataset Builder — AlphaByteCore")
    print("Building all dataset files...\n")

    check_dirs()
    run("build_chapters.py",       "Building chapter metadata (18 chapters)")
    run("build_key_verses.py",     "Building annotated shlokas corpus")
    run("build_glossary.py",       "Building Sanskrit concept glossary")
    run("build_qa_pairs.py",       "Building Q&A training pairs + JSONL files")
    run("build_problem_mapping.py","Building problem-verse retrieval index")
    run("build_stats.py",          "Generating dataset statistics")
    print_summary()
    print("🙏 Sarve bhavantu sukhinah — Dataset build complete.\n")
