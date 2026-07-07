import sys
from pathlib import Path
import subprocess

def manage_library():
    if len(sys.argv) < 2:
        print("Error: ファイル名（拡張子なし）を指定してください。")
        print("Example: lib-open segment_tree")
        return

    is_test_mode = (sys.argv[1] == "test")
    
    if is_test_mode:
        if len(sys.argv) < 3:
            print("Error: テストファイル名（拡張子なし）を指定してください。")
            return
        filename = sys.argv[2]
        target_dir = Path(__file__).parent / "test"
    else:
        filename = sys.argv[1]
        target_dir = Path(__file__).parent / "src"

    if not filename.endswith(".py"):
        filename += ".py"

    target_dir.mkdir(exist_ok=True)
    file_path = target_dir / filename

    # 🌟 ファイルの存在チェックで挙動を分岐
    if file_path.exists():
        print(f"Opening existing file: {file_path.name}")
    else:
        if is_test_mode:
            template = (
                "# PROBLEM \n"
                "\n"
                "import sys\n"
                "import os\n"
                "sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))\n"
                "\n"
                "# from src. import \n"
            )
        else:
            template = (
                "# name: \n"
                "# prefix: \n"
                "# ---\n"
                "\n"
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