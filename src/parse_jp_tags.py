import json
import os
import re

# Removed unused sys import
from typing import (  # Removed Set, List as they are no longer needed after type hint updates
    TypedDict,
    cast,
)


# Use a simpler approach for handling encoding errors
def safe_print(message: str) -> None:
    """Print a message, handling encoding errors gracefully"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fall back to ASCII with escaped characters if Unicode fails
        print(str(message).encode("ascii", "backslashreplace").decode("ascii"))


class Category(TypedDict):
    name: str
    parent: str | None  # Updated Optional[str]
    level: int


class TagMeta(TypedDict):
    related_tags: list[str]  # Updated List[str]
    see_also: list[str]  # Updated List[str]


class TagData(TypedDict):
    name: str
    slug: str
    name_en: str | None  # Updated Optional[str]
    description: str
    category: str
    meta: TagMeta


def create_root_category() -> Category:
    return Category(name="", parent=None, level=0)


# Include構文の正規表現
include_pattern = re.compile(r"\[\[include\s+:scp-jp:fragment:([^\]]+)\]\]")


def read_and_expand_includes(
    filepath: str, base_dir: str = ".", visited: set[str] | None = None
) -> str:  # Updated Optional[Set[str]]
    """
    指定されたファイルを読み込み、[[include]]構文を展開して内容を返す。
    循環参照を防止する。

    Args:
        filepath (str): 読み込むファイルのパス。
        base_dir (str): ファイルパスの基準ディレクトリ。
        visited (Optional[Set[str]]): 既に訪れたファイルのセット（循環参照防止用）。

    Returns:
        str: Includeを展開したファイルの内容。
    """
    if visited is None:
        visited = set()

    full_path = os.path.normpath(os.path.join(base_dir, filepath))
    try:
        safe_print(f"DEBUG: Attempting to read file: {full_path}")
    except Exception:
        safe_print(
            "DEBUG: Attempting to read file: (path contains non-printable characters)"
        )

    if full_path in visited:
        safe_print(f"Warning: Circular include detected and skipped for {filepath}")
        return ""  # 循環参照の場合は空文字列を返す

    visited.add(full_path)

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
            safe_print(
                f"DEBUG: Successfully read file: {full_path} ({len(content)} bytes)"
            )
    except FileNotFoundError:
        safe_print(f"Warning: Included file not found: {filepath}")
        return ""  # ファイルが見つからない場合は空文字列

    # Include構文を探して再帰的に展開
    expanded_content = ""
    last_end = 0
    include_count = 0

    for match in include_pattern.finditer(content):
        include_count += 1
        start, end = match.span()
        included_filename_base = match.group(1)
        try:
            safe_print(
                f"DEBUG: Found include directive: {match.group(0)}, extracted filename base: {included_filename_base}"
            )
        except Exception:
            safe_print(
                "DEBUG: Found include directive (contains non-printable characters)"
            )

        # .txt拡張子がない場合に追加（Wikidotの挙動に合わせる）
        if not included_filename_base.endswith(".txt"):
            included_filename = f"fragment_{included_filename_base}.txt"
        else:
            if not included_filename_base.startswith("fragment_"):
                if included_filename_base.startswith("tag-list-"):
                    included_filename = f"fragment_{included_filename_base}"
                else:
                    included_filename = included_filename_base
            else:
                included_filename = included_filename_base

        included_full_path = os.path.normpath(os.path.join(base_dir, included_filename))
        try:
            safe_print(f"DEBUG: Resolved include path: {included_full_path}")
        except Exception:
            safe_print(
                "DEBUG: Resolved include path (contains non-printable characters)"
            )

        expanded_content += content[last_end:start]
        included_content = read_and_expand_includes(
            included_filename, base_dir, visited.copy()
        )
        expanded_content += included_content
        safe_print(f"DEBUG: Added {len(included_content)} bytes from included file")
        last_end = end

    expanded_content += content[last_end:]
    safe_print(f"DEBUG: Total includes found: {include_count}")
    safe_print(f"DEBUG: Final expanded content size: {len(expanded_content)} bytes")
    return expanded_content


def parse_jp_tag_list(
    start_filepath: str = "tag-list.txt",
    output_filepath: str = os.path.join("data", "processed", "jp_tags.json"),
    base_dir: str = os.path.join("data", "raw", "wikidot_sources", "scp-jp"),
) -> None:
    """
    日本語版タグリストファイルを解析し、タグ情報をJSON形式で出力する。
    """
    safe_print(
        f"Starting to parse Japanese tag list from: {os.path.join(base_dir, start_filepath)}"
    )
    full_content = read_and_expand_includes(start_filepath, base_dir=base_dir)
    safe_print(f"Expanded content size: {len(full_content)} bytes")

    tags_data: list[TagData] = []  # Updated List[TagData]
    current_tag: TagData | None = None  # Updated Optional[TagData]

    # 正規表現パターン - 修正版
    # セクションヘッダは "+ タイトル" または "++ タイトル" の形式
    section_pattern = re.compile(r"^\+\+?\s+(.*?)(?:\[\[#.*)?$")
    # タグ定義行は、行頭の任意の空白（半角・全角含む）＋* で始まるように修正
    # アイコン表現（,,で囲まれた部分）が0回以上入る場合にも対応
    tag_pattern = re.compile(
        r"^[ \t\u3000]*\*[ \t\u3000]*(?:,,[^,]+,,[ \t\u3000]*)*\*\*\[\[\[/system:page-tags/tag/([^|]+)\|([^\]]+)\]\]\]\*\*[ \t\u3000]*(?://\(([^)]+)\)//[ \t\u3000]*)?-\s*(.*)"
    )
    # メタ情報行は "* // キー: 値 //" の形式
    meta_pattern = re.compile(r"^[ \t\u3000]*\*[ \t\u3000]*//\s*([^:]+):\s*(.*)//")

    current_category: Category = create_root_category()
    stack: list[Category] = [current_category]  # Updated List[Category]

    tag_count = 0
    section_count = 0
    meta_count = 0

    for line_num, line in enumerate(full_content.split("\n"), 1):
        line = line.rstrip()

        # セクションヘッダの処理
        section_match = section_pattern.match(line)
        if section_match:
            name = section_match.group(1).strip()
            level = 1 if line.startswith("+ ") else 2 if line.startswith("++ ") else 0

            if level > 0:
                safe_print(
                    f"DEBUG: Found section header at line {line_num}: '{name}' (level {level})"
                )
                section_count += 1

                # 階層レベルに基づいて親子関係を更新
                while stack and stack[-1]["level"] >= level:
                    stack.pop()

                parent = stack[-1]["name"] if stack else None
                current_category = Category(name=name, parent=parent, level=level)
                safe_print(f"DEBUG: Updated current category to: {current_category}")
            continue

        # タグ定義行の処理
        tag_match = tag_pattern.match(line)
        if tag_match:
            if current_tag:
                tags_data.append(current_tag)
                safe_print(f"DEBUG: Added tag to tags_data: {current_tag['name']}")

            tag_slug = tag_match.group(1).strip()
            tag_name = tag_match.group(2).strip()
            tag_en = tag_match.group(3) if tag_match.group(3) else None
            description = tag_match.group(4).strip() if tag_match.group(4) else ""

            safe_print(
                f"DEBUG: Found tag at line {line_num}: '{tag_name}' (slug: {tag_slug}) in category '{current_category['name']}'"
            )
            if tag_en:
                safe_print(f"DEBUG: English name: {tag_en}")
            tag_count += 1

            current_tag = TagData(
                name=tag_name,
                slug=tag_slug,
                name_en=tag_en,
                description=description,
                category=current_category["name"],
                meta=TagMeta(related_tags=[], see_also=[]),
            )
            continue

        # メタ情報行の処理
        if current_tag:
            meta_match = meta_pattern.match(line)
            if meta_match:
                key = meta_match.group(1).strip().lower().replace(" ", "-")
                values = [
                    v.strip().replace("'", "") for v in meta_match.group(2).split(",")
                ]
                safe_print(
                    f"DEBUG: Found meta info at line {line_num} for tag '{current_tag['name']}': {key} = {values}"
                )
                meta_count += 1

                if key not in current_tag["meta"]:
                    current_tag["meta"][key] = []
                # Ensure we have a list to extend
                meta_list = cast(
                    list[str], current_tag["meta"].setdefault(key, [])
                )  # Updated cast(List[str], ...)
                meta_list.extend(values)

    # 最後のタグを追加
    if current_tag:
        tags_data.append(current_tag)
        safe_print(f"DEBUG: Added final tag to tags_data: {current_tag['name']}")

    safe_print(
        f"DEBUG: Parsing complete. Found {section_count} sections, {tag_count} tags, and {meta_count} meta entries."
    )

    # JSONファイルへの書き込み
    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            json.dump(tags_data, f, ensure_ascii=False, indent=2)
        safe_print(
            f"Successfully processed {len(tags_data)} tags. Saved to {output_filepath}"
        )
    except Exception as e:
        safe_print(f"An error occurred during JSON writing: {e}")


def main():
    parse_jp_tag_list()


if __name__ == "__main__":
    main()
