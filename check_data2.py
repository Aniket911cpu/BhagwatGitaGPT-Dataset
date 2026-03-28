import json
import os
import sys

dataset_dir = r"c:\Users\anike\Music\BhagwatGitaGPT Dataset\data"
out_filepath = os.path.join(dataset_dir, "analysis_out.txt")

with open(out_filepath, 'w', encoding='utf-8') as out_f:
    def log(msg):
        out_f.write(str(msg) + '\n')
    
    def check_jsonl(filepath):
        log(f"\n--- Checking {os.path.basename(filepath)} ---")
        issues = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                log(f"Total records: {len(lines)}")
                
                for i, line in enumerate(lines):
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError as e:
                        issues.append(f"Line {i+1}: JSON Decode Error - {e}")
                        continue
                    
                    if "messages" in obj:
                        messages = obj["messages"]
                        if not isinstance(messages, list):
                            issues.append(f"Line {i+1}: 'messages' is not a list")
                            continue
                        if len(messages) < 2:
                            issues.append(f"Line {i+1}: 'messages' has fewer than 2 items")
                        for j, msg in enumerate(messages):
                            if "role" not in msg or "content" not in msg:
                                issues.append(f"Line {i+1}: message {j} missing role or content")
                            elif not str(msg["content"]).strip():
                                issues.append(f"Line {i+1}: message {j} has empty content")
                    elif "instruction" in obj:
                        for key in ["instruction", "input", "output"]:
                            if key not in obj:
                                issues.append(f"Line {i+1}: missing key '{key}'")
                            elif obj[key] is not None and not str(obj[key]).strip() and key != "input":
                                issues.append(f"Line {i+1}: empty '{key}'")
                    else:
                        issues.append(f"Line {i+1}: unrecognized format keys {list(obj.keys())}")
                        
        except Exception as e:
            log(f"Error reading file: {e}")
            
        for issue in issues[:20]:
            log(issue)
        if len(issues) > 20:
            log(f"... and {len(issues) - 20} more issues")
        if not issues:
            log("No structural issues found.")

    def check_json(filepath):
        log(f"\n--- Checking {os.path.basename(filepath)} ---")
        issues = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                log(f"Total records: {len(data)}")
                if not isinstance(data, list):
                    log("Root is not a list. Type: " + str(type(data)))
                    if isinstance(data, dict):
                        for k, v in data.items():
                            if isinstance(v, str) and not v.strip():
                                issues.append(f"Key '{k}' has empty string value.")
                    return
                for i, obj in enumerate(data):
                    for k, v in obj.items():
                        if isinstance(v, str) and not v.strip():
                            if k not in ["input", "context"]:
                                issues.append(f"Record {i+1}: empty value for key '{k}'")
        except Exception as e:
            log(f"Error reading file: {e}")
        for issue in issues[:20]:
            log(issue)
        if len(issues) > 20:
            log(f"... and {len(issues) - 20} more issues")
        if not issues:
            log("No structural issues found.")

    check_jsonl(os.path.join(dataset_dir, "processed", "finetune_chatml_format.jsonl"))
    check_jsonl(os.path.join(dataset_dir, "processed", "finetune_instruction_format.jsonl"))
    check_json(os.path.join(dataset_dir, "qa_pairs", "qa_training_pairs.json"))
    check_json(os.path.join(dataset_dir, "processed", "problem_verse_mapping.json"))
