import subprocess
import sys
import os


def run_step(description, command, cwd=None):
    print(f"\n=== {description} ===")
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} で失敗しました: {e}")
        sys.exit(1)


def main():
    # 1. Wikidotページ取得
    run_step(
        "Wikidotページ取得 (src/retrieve_wikidot_page.py)",
        f"{sys.executable} src/retrieve_wikidot_page.py",
        cwd=os.path.dirname(__file__),
    )
    # 2. 英語タグパース
    run_step(
        "英語タグパース (src/parse_en_tags.py)",
        f"{sys.executable} src/parse_en_tags.py",
        cwd=os.path.dirname(__file__),
    )
    # 3. 日本語タグパース
    run_step(
        "日本語タグパース (src/parse_jp_tags.py)",
        f"{sys.executable} src/parse_jp_tags.py",
        cwd=os.path.dirname(__file__),
    )
    # 4. 辞書生成
    run_step(
        "辞書生成 (src/create_en_to_jp_dict.py)",
        f"{sys.executable} src/create_en_to_jp_dict.py",
        cwd=os.path.dirname(__file__),
    )
    # 5. テスト実行
    run_step(
        "pytestによるテスト実行",
        f"{sys.executable} -m pytest",
        cwd=os.path.dirname(__file__),
    )
    print("\n=== 全処理が正常に完了しました ===")


if __name__ == "__main__":
    main()
