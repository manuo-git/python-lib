import sys
from pathlib import Path
import subprocess

def manage_library():
    if len(sys.argv) < 2:
        print("Error: ファイル名（拡張子なし）を指定してください。")
        print("Example: lib-open segment_tree")
        return

    filename = sys.argv[1]
    if not filename.endswith(".py"):
        filename += ".py"

    src_dir = Path(__file__).parent / "src"
    src_dir.mkdir(exist_ok=True)
    file_path = src_dir / filename

    # 🌟 ファイルの存在チェックで挙動を分岐
    if file_path.exists():
        print(f"Opening existing file: {file_path.name}")
    else:
        # 存在しない場合は新規作成（雛形を書き込む）
        template = (
            "# name: \n"
            "# prefix: \n"
            "# ---\n"
        )
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(template)
        print(f"Created new file with template: {file_path.name}")

    print(str(file_path))
    # VSCodeで開く
    try:
        subprocess.run(["code", str(file_path)], check=True, shell=True)
    except FileNotFoundError:
        print("Error: 'code' コマンドが見つかりません。VSCodeのPATHを確認してください。")

if __name__ == "__main__":
    manage_library()