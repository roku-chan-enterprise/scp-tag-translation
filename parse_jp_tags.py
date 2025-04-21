import re
import json
import os
from typing import TypedDict

class Category(TypedDict):
    name: str
    parent: str | None
    level: int

class TagMeta(TypedDict):
    related_tags: list[str]
    see_also: list[str]

class TagData(TypedDict):
    name: str
    description: str
    category: str
    meta: TagMeta

def create_root_category() -> Category:
    return Category(name='', parent=None, level=0)

# Include構文の正規表現
include_pattern = re.compile(r"\[\[include\s+:scp-jp:fragment:([^\]]+)\]\]")

def read_and_expand_includes(filepath: str, base_dir: str = ".", visited: set[str] | None = None) -> str: # Optional を | None に変更
    """
    指定されたファイルを読み込み、[[include]]構文を展開して内容を返す。
    循環参照を防止する。

    Args:
        filepath (str): 読み込むファイルのパス。
        base_dir (str): ファイルパスの基準ディレクトリ。
        visited (Optional[set[str]]): 既に訪れたファイルのセット（循環参照防止用）。

    Returns:
        str: Includeを展開したファイルの内容。
    """
    if visited is None:
        visited = set()

    full_path = os.path.normpath(os.path.join(base_dir, filepath))

    if full_path in visited:
        print(f"Warning: Circular include detected and skipped for {filepath}")
        return "" # 循環参照の場合は空文字列を返す

    visited.add(full_path)

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Warning: Included file not found: {filepath}")
        return "" # ファイルが見つからない場合は空文字列

    # Include構文を探して再帰的に展開
    expanded_content = ""
    last_end = 0
    for match in include_pattern.finditer(content):
        start, end = match.span()
        included_filename_base = match.group(1)
        # .txt拡張子がない場合に追加（Wikidotの挙動に合わせる）
        # Included files are expected to be in the 'scp-jp' directory
        included_dir = "scp-jp"
        if not included_filename_base.endswith('.txt'):
            included_filename = os.path.join(included_dir, f"fragment_{included_filename_base}.txt")
        else:
            # If it already has .txt, assume it's the full fragment name like fragment_tag-list-basic.txt
            # We still need to prepend the directory
            # Check if 'fragment_' prefix is already there, if not, add it (based on original logic intent)
            if not included_filename_base.startswith('fragment_'):
                # This case might be less common now, but preserving similar logic
                if included_filename_base.startswith('tag-list-'): # Original check
                    included_filename = os.path.join(included_dir, f"fragment_{included_filename_base}")
                else: # Fallback
                    included_filename = os.path.join(included_dir, included_filename_base)
            else:
                included_filename = os.path.join(included_dir, included_filename_base)


        expanded_content += content[last_end:start]
        # 新しいvisitedセットを渡して再帰呼び出し
        expanded_content += read_and_expand_includes(included_filename, base_dir, visited.copy())
        last_end = end

    expanded_content += content[last_end:]
    return expanded_content

def parse_jp_tag_list(start_filepath: str = os.path.join("scp-jp", "tag-list.txt"), output_filepath: str = "jp_tags.json"):
    """
    日本語版タグリストファイルを解析し、タグ情報をJSON形式で出力する。

    Args:
        start_filepath (str): 解析を開始するファイルパス。
        output_filepath (str): 出力ファイルパス (JSON形式)。
    """
    full_content = read_and_expand_includes(start_filepath)
    tags_data: list[TagData] = []
    current_tag: TagData | None = None  # Type hint matches initialization

    # 正規表現パターン
    section_pattern = re.compile(r'^#+\s*(.*)')  # セクションヘッダ
    tag_pattern = re.compile(r'^\*\*\*\s*([^\s-]+)(?:\s*--\s*(.*))?')  # タグ定義行
    meta_pattern = re.compile(r'^\*\s*//\s*([^:]+):\s*(.*)//')  # メタ情報

    current_category: Category = {
        'name': '',
        'parent': None,
        'level': 0
    }
    stack: list[Category] = []

    for line in full_content.split('\n'):
        line = line.rstrip()

        # セクションヘッダの処理
        section_match = section_pattern.match(line)
        if section_match:
            level = line.count('#', 0, section_match.end())
            name = section_match.group(1).strip()

            # 階層レベルに基づいて親子関係を更新
            while stack and stack[-1]['level'] >= level:
                stack.pop()

            parent = stack[-1]['name'] if stack else None
            current_category: Category = {
                'name': name,
                'parent': parent,
                'level': level
            }
            stack.append(current_category)
            continue

        # タグ定義行の処理
        tag_match = tag_pattern.match(line)
        if tag_match:
            if current_tag:
                tags_data.append(current_tag)

            tag_name = tag_match.group(1).strip()
            description = tag_match.group(2).strip() if tag_match.group(2) else ''

            current_tag = {
                'name': tag_name,
                'description': description,
                'category': current_category['name'],
                'meta': TagMeta(related_tags=[], see_also=[])
            }
            continue

        # メタ情報行の処理
        if current_tag:
            meta_match = meta_pattern.match(line)
            if meta_match:
                key = meta_match.group(1).strip().lower().replace(' ', '-')
                values = [v.strip().replace("'", "") for v in meta_match.group(2).split(',')]

                if key not in current_tag['meta']:
                    current_tag['meta'][key] = []
                # Ensure we have a list to extend and help type checker with cast
                from typing import cast
                current_meta_list = cast(list[str], current_tag['meta'].setdefault(key, []))
                current_meta_list.extend(values)

    # 最後のタグを追加
    if current_tag:
        tags_data.append(current_tag)

    # JSONファイルへの書き込み (仮)
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
             # 現時点では空のリストを書き込む
            json.dump(tags_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully processed includes. Tag parsing logic pending. Saved empty list to {output_filepath}")
    except Exception as e:
        print(f"An error occurred during JSON writing: {e}")

if __name__ == "__main__":
    parse_jp_tag_list()