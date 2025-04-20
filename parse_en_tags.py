import re
import json
from typing import TypeAlias # TypeAlias をインポート

# 型エイリアスを定義 (Python 3.10+ の記法)
TagMeta: TypeAlias = dict[str, list[str]]
TagData: TypeAlias = dict[str, str | TagMeta]

def parse_tag_list(input_filepath: str = "05command_tech-hub-tag-list.txt", output_filepath: str = "en_tags.json"):
    """
    Wikidot形式のタグリストファイルを解析し、タグ情報をJSON形式で出力する。

    Args:
        input_filepath (str): 入力ファイルパス (Wikidot形式のタグリスト)
        output_filepath (str): 出力ファイルパス (JSON形式)
    """
    tags_data: list[TagData] = [] # list を使用
    current_tag: TagData | None = None # | None を使用

    # 正規表現パターン
    tag_pattern = re.compile(r"^\s*\*\s*\*\*\[https?://[^ ]+\s+([^\]]+)\]\*\*")
    desc_pattern = re.compile(r"--\s*(.*)")
    meta_pattern = re.compile(r"^\s*\*\s*//\s*([^:]+):\s*(.*)\s*//")

    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # タグ定義行の処理
                tag_match = tag_pattern.match(line)
                if tag_match:
                    # 前のタグ情報をリストに追加 (存在する場合)
                    if current_tag:
                        tags_data.append(current_tag)

                    tag_name = tag_match.group(1)
                    desc_match = desc_pattern.search(line)
                    description = desc_match.group(1).strip() if desc_match else ""

                    current_tag = {
                        "name": tag_name,
                        "description": description,
                        "meta": {} # meta を空の辞書で初期化
                    }
                    continue # 次の行へ

                # メタ情報行の処理
                if current_tag: # タグ定義行の後でのみメタ情報を探す
                    meta_match = meta_pattern.match(line)
                    if meta_match:
                        meta_key = meta_match.group(1).strip().lower().replace(' ', '-') # キーを小文字化、スペースをハイフンに
                        meta_value_str = meta_match.group(2).strip()
                        # カンマ区切りの値をリストに変換
                        meta_values = [v.strip().replace("'", "") for v in meta_value_str.split(',') if v.strip()]

                        # current_tag と current_tag["meta"] が None でないことを確認
                        if current_tag and isinstance(current_tag["meta"], dict):
                            if meta_key not in current_tag["meta"]:
                                current_tag["meta"][meta_key] = []
                            current_tag["meta"][meta_key].extend(meta_values)
                        continue # 次の行へ

            # 最後のタグ情報をリストに追加
            if current_tag:
                tags_data.append(current_tag)

        # JSONファイルへの書き込み
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(tags_data, f, ensure_ascii=False, indent=2)

        print(f"Successfully parsed tags and saved to {output_filepath}")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parse_tag_list()