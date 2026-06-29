import os
import json
from pathlib import Path

def generate_snippets():
    # スクリプトの場所を基準に絶対パスを計算
    base_dir = Path(__file__).parent
    src_dir = base_dir / "src"
    
    # 🌟 VSCodeのユーザー設定フォルダへ直接書き出す設定
    # Windows側のVSCodeをWSLから使う場合の一般的なパス（ユーザー名はご自身の環境に合わせてください）
    # ※ もし動かない場合は、通常通りリポジトリ内に吐き出す設定（output_dir = base_dir / "snippets"）にしてください。
    win_user = os.environ.get("USER", "default")
    output_dir = Path(f"/mnt/c/Users/{win_user}/AppData/Roaming/Code/User/snippets")
    
    if not output_dir.exists():
        # フォールバック: VSCodeフォルダが見つからない場合はリポジトリ内に保存
        output_dir = base_dir / "snippets"
        output_dir.mkdir(exist_ok=True)
        
    output_file = output_dir / "python.json"
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

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(snippets, f, indent=4, ensure_ascii=False)
    
    print(f"\nSuccess! Snippets updated: {output_file}")

if __name__ == "__main__":
    generate_snippets()