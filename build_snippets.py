import os
import json
from pathlib import Path

def generate_snippets():
    # スクリプトの場所を基準に絶対パスを計算
    base_dir = Path(__file__).parent
    src_dir = base_dir / "src"

    snippets = make_snippets(src_dir)
    
    # 🌟 config.json からパスを読み込む
    config_file = base_dir / "config.json"
    vscode_snippet_dir = None
    
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as cf:
            config = json.load(cf)
            # JSONからパスを取得して Path オブジェクトに変換
            if "vscode_snippets_dir" in config:
                vscode_snippet_dir = Path(config["vscode_snippets_dir"])

    if not vscode_snippet_dir or not vscode_snippet_dir.exists():
        print("Warning: config.json が見つからないか、パスが無効です。")
    else:
        output_file = vscode_snippet_dir / "python.json"
        write_to_file(output_file, snippets)
    backup_snippet_dir = base_dir / "snippets"
    backup_snippet_dir.mkdir(exist_ok=True)
    output_file = backup_snippet_dir / "python.json"
    write_to_file(output_file, snippets)

def make_snippets(src_dir):
    snippets = {}

    for file_path in src_dir.glob("*.py"):
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        name = None
        prefix = None
        code_lines = []
        is_code = False
        
        for line in lines:
            if not is_code:
                if line.startswith("# name:"):
                    name = line.replace("# name:", "").strip()
                elif line.startswith("# prefix:"):
                    prefix = line.replace("# prefix:", "").strip()
                elif line.startswith("# ---"):
                    is_code = True
            else:
                code_lines.append(line.rstrip("\n"))
        
        if not name or not prefix:
            print(f"Skipped: {file_path.name} (name または prefix が空欄です)")
            continue

        snippets[name] = {
            "description": f"[{file_path.name}] 競プロライブラリ: {name}",
            "prefix": [p.strip() for p in prefix.split(",")],
            "body": code_lines
        }
        print(f"Loaded: {name} (file: {file_path.name})")
    return snippets

def write_to_file(output_file, snippets):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(snippets, f, indent=4, ensure_ascii=False)
    
    print(f"\nSuccess! Snippets updated: {output_file}")

if __name__ == "__main__":
    generate_snippets()