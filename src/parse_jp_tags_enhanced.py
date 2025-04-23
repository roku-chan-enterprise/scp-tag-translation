import json
import os
import re
from typing import TypedDict, cast, List, Dict, Optional, Set, Tuple, Any

# デバッグ出力用の関数
def safe_print(message: str) -> None:
    """Print a message, handling encoding errors gracefully"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fall back to ASCII with escaped characters if Unicode fails
        print(str(message).encode("ascii", "backslashreplace").decode("ascii"))


# データ構造の定義
class Category(TypedDict):
    name: str
    parent: Optional[str]
    level: int


class RelatedPage(TypedDict):
    slug: str
    display_name: Optional[str]


class RelatedTag(TypedDict):
    slug: str
    relation_type: str


class Restriction(TypedDict):
    icon: str
    meaning: str


class SourceLocation(TypedDict):
    file: str
    line: int


class TagMeta(TypedDict):
    related_pages: List[RelatedPage]
    related_tags: List[RelatedTag]
    target_page_types: List[str]
    footnotes: List[str]
    other_notes: List[str]


class EnhancedTagData(TypedDict):
    slug: str
    name_jp: str
    name_en: Optional[str]
    description_raw: str
    description_plain: str
    category_path: List[str]
    restrictions: List[Restriction]
    meta: TagMeta
    source_location: SourceLocation


def create_root_category() -> Category:
    return Category(name="", parent=None, level=0)


# Include構文の正規表現
include_pattern = re.compile(r"\[\[include\s+:scp-jp:fragment:([^\]]+)\]\]")


def read_and_expand_includes(
    filepath: str, base_dir: str = ".", visited: Optional[Set[str]] = None
) -> str:
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


# Wikidotリンクを抽出する正規表現
wikidot_link_pattern = re.compile(r"\[(?:/|[^\s\[\]]+\s+)?([^\[\]|]+)(?:\|([^\[\]]+))?\]")
wikidot_triple_link_pattern = re.compile(r"\[\[\[([^\[\]|]+)(?:\|([^\[\]]+))?\]\]\]")

# 脚注を抽出する正規表現
footnote_pattern = re.compile(r"\[\[footnote\]\](.*?)\[\[/footnote\]\]", re.DOTALL)

# 関連タグを抽出するためのパターン
related_tag_patterns = [
    (r"//([^/]+)//タグと(?:は)?併用(?:でき)?(?:ない|ません)", "併用不可"),
    (r"//([^/]+)//タグ(?:を|の)(?:代わりに|代替として)(?:使用|使って)(?:して)?ください", "代替推奨"),
    (r"//([^/]+)//タグ(?:を|も)(?:参照|確認)(?:して)?ください", "参照推奨"),
    (r"必ず//([^/]+)//タグと併用(?:して)?(?:ください|する必要があります|されねばなりません)", "併用必須"),
    (r"適切(?:な)?(?:ら)?(?:ば)?//([^/]+)//タグと併用(?:して)?ください", "併用推奨"),
]

# 対象ページ種別を抽出するためのパターン
target_page_patterns = [
    (r"(SCP報告書|SCPオブジェクト)の記事に付与", ["scp"]),
    (r"//scp//(?:タグ|ページ|記事)(?:が付与されて|に付与|にしか付与でき)(?:いる|ない)", ["scp"]),
    (r"//tale//(?:タグ|ページ|記事)(?:が付与されて|に付与|にしか付与でき)(?:いる|ない)", ["tale"]),
    (r"//goi-format//(?:タグ|ページ|記事)(?:が付与されて|に付与|にしか付与でき)(?:いる|ない)", ["goi-format"]),
    (r"//補足//(?:タグ|ページ|記事)(?:が付与されて|に付与|にしか付与でき)(?:いる|ない)", ["補足"]),
]

# 制限アイコンとその意味のマッピング
restriction_icon_meanings = {
    "︁": "使用禁止",
    "": "編集禁止",
    "": "制限緩和/翻訳",
}


def extract_wikidot_links(text: str) -> List[RelatedPage]:
    """
    テキストからWikidotリンクを抽出する
    
    Args:
        text (str): 解析するテキスト
        
    Returns:
        List[RelatedPage]: 抽出されたリンク情報のリスト
    """
    links = []
    
    # 通常リンク [page-slug] や [page-slug|表示名] を抽出
    for match in wikidot_link_pattern.finditer(text):
        slug = match.group(1).strip()
        display_name = match.group(2).strip() if match.group(2) else None
        links.append(RelatedPage(slug=slug, display_name=display_name))
    
    # トリプルリンク [[[page-slug]]] や [[[page-slug|表示名]]] を抽出
    for match in wikidot_triple_link_pattern.finditer(text):
        slug = match.group(1).strip()
        display_name = match.group(2).strip() if match.group(2) else None
        links.append(RelatedPage(slug=slug, display_name=display_name))
    
    return links


def extract_footnotes(text: str) -> List[str]:
    """
    テキストから脚注を抽出する
    
    Args:
        text (str): 解析するテキスト
        
    Returns:
        List[str]: 抽出された脚注のリスト
    """
    footnotes = []
    
    for match in footnote_pattern.finditer(text):
        footnote_text = match.group(1).strip()
        footnotes.append(footnote_text)
    
    return footnotes


def extract_related_tags(text: str) -> List[RelatedTag]:
    """
    テキストから関連タグとその関係性を抽出する
    
    Args:
        text (str): 解析するテキスト
        
    Returns:
        List[RelatedTag]: 抽出された関連タグ情報のリスト
    """
    related_tags = []
    
    for pattern, relation_type in related_tag_patterns:
        for match in re.finditer(pattern, text):
            tag_name = match.group(1).strip()
            related_tags.append(RelatedTag(slug=tag_name, relation_type=relation_type))
    
    # タグへの直接リンクも抽出
    for match in re.finditer(r"\[\[\[/system:page-tags/tag/([^|]+)\|([^\]]+)\]\]\]", text):
        tag_slug = match.group(1).strip()
        tag_name = match.group(2).strip()
        related_tags.append(RelatedTag(slug=tag_slug, relation_type="言及"))
    
    return related_tags


def extract_target_page_types(text: str) -> List[str]:
    """
    テキストから対象ページ種別を抽出する
    
    Args:
        text (str): 解析するテキスト
        
    Returns:
        List[str]: 抽出された対象ページ種別のリスト
    """
    target_types = []
    
    for pattern, types in target_page_patterns:
        if re.search(pattern, text):
            target_types.extend(types)
    
    return list(set(target_types))  # 重複を除去


def extract_other_notes(text: str) -> List[str]:
    """
    テキストからその他の注意点を抽出する
    
    Args:
        text (str): 解析するテキスト
        
    Returns:
        List[str]: 抽出された注意点のリスト
    """
    notes = []
    
    # 必須条件の抽出
    for match in re.finditer(r"必ず.*(?:ください|必要があります|ねばなりません)", text):
        notes.append(match.group(0))
    
    # 禁止事項の抽出
    for match in re.finditer(r"(?:使用|付与|併用)(?:でき)?(?:ない|ません)", text):
        context = text[max(0, match.start() - 50):min(len(text), match.end() + 50)]
        notes.append(context.strip())
    
    return notes


def strip_wikidot_syntax(text: str) -> str:
    """
    Wikidot構文を除去してプレーンテキストを生成する
    
    Args:
        text (str): Wikidot構文を含むテキスト
        
    Returns:
        str: プレーンテキスト
    """
    # 脚注を除去
    text = re.sub(r"\[\[footnote\]\].*?\[\[/footnote\]\]", "", text, flags=re.DOTALL)
    
    # リンクを処理 ([[[slug|name]]] -> name, [[[slug]]] -> slug)
    text = re.sub(r"\[\[\[([^|]+)\|([^\]]+)\]\]\]", r"\2", text)
    text = re.sub(r"\[\[\[([^\]]+)\]\]\]", r"\1", text)
    
    # 通常リンクを処理 ([slug|name] -> name, [slug] -> slug)
    text = re.sub(r"\[(?:[^\s\[\]]+\s+)?([^|]+)\|([^\]]+)\]", r"\2", text)
    text = re.sub(r"\[(?:[^\s\[\]]+\s+)?([^\]]+)\]", r"\1", text)
    
    # 太字、斜体を処理
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"//([^/]+)//", r"\1", text)
    
    # その他のWikidot構文を除去
    text = re.sub(r"\[\[.*?\]\]", "", text)
    
    return text.strip()


def extract_restriction_icons(line: str) -> List[Restriction]:
    """
    行から制限アイコンとその意味を抽出する
    
    Args:
        line (str): 解析する行
        
    Returns:
        List[Restriction]: 抽出された制限情報のリスト
    """
    restrictions = []
    
    # アイコンパターン ,,アイコン,, を検出
    for match in re.finditer(r",,([^,]+),,", line):
        icon = match.group(1)
        if icon in restriction_icon_meanings:
            meaning = restriction_icon_meanings[icon]
            restrictions.append(Restriction(icon=icon, meaning=meaning))
    
    return restrictions


def build_category_path(category: Category, stack: List[Category]) -> List[str]:
    """
    カテゴリの階層パスを構築する
    
    Args:
        category (Category): 現在のカテゴリ
        stack (List[Category]): カテゴリスタック
        
    Returns:
        List[str]: カテゴリパス
    """
    path = []
    
    # スタックからパスを構築
    for cat in stack:
        if cat["name"]:  # ルートカテゴリは空文字列なので除外
            path.append(cat["name"])
    
    # 現在のカテゴリを追加（スタックに含まれていない場合）
    if category["name"] and (not path or path[-1] != category["name"]):
        path.append(category["name"])
    
    return path


def parse_jp_tag_list_enhanced(
    start_filepath: str = "tag-list.txt",
    output_filepath: str = os.path.join("data", "processed", "jp_tags_enhanced.json"),
    base_dir: str = os.path.join("data", "raw", "wikidot_sources", "scp-jp"),
) -> None:
    """
    日本語版タグリストファイルを解析し、拡張されたタグ情報をJSON形式で出力する。
    """
    safe_print(
        f"Starting to parse Japanese tag list from: {os.path.join(base_dir, start_filepath)}"
    )
    full_content = read_and_expand_includes(start_filepath, base_dir=base_dir)
    safe_print(f"Expanded content size: {len(full_content)} bytes")

    tags_data: List[EnhancedTagData] = []
    current_source_file = start_filepath

    # 正規表現パターン
    section_pattern = re.compile(r"^\+\+?\s+(.*?)(?:\[\[#.*)?$")
    tag_pattern = re.compile(
        r"^[ \t\u3000]*\*[ \t\u3000]*(?:,,[^,]+,,[ \t\u3000]*)*\*\*\[\[\[/system:page-tags/tag/([^|]+)\|([^\]]+)\]\]\]\*\*[ \t\u3000]*(?://\(([^)]+)\)//[ \t\u3000]*)?-\s*(.*)"
    )

    current_category: Category = create_root_category()
    category_stack: List[Category] = [current_category]

    tag_count = 0
    section_count = 0

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
                while category_stack and category_stack[-1]["level"] >= level:
                    category_stack.pop()

                parent = category_stack[-1]["name"] if category_stack else None
                current_category = Category(name=name, parent=parent, level=level)
                category_stack.append(current_category)
                safe_print(f"DEBUG: Updated current category to: {current_category}")
            continue

        # タグ定義行の処理
        tag_match = tag_pattern.match(line)
        if tag_match:
            tag_slug = tag_match.group(1).strip()
            tag_name = tag_match.group(2).strip()
            tag_en = tag_match.group(3) if tag_match.group(3) else None
            description_raw = tag_match.group(4).strip() if tag_match.group(4) else ""

            safe_print(
                f"DEBUG: Found tag at line {line_num}: '{tag_name}' (slug: {tag_slug}) in category '{current_category['name']}'"
            )
            if tag_en:
                safe_print(f"DEBUG: English name: {tag_en}")
            tag_count += 1

            # 制限アイコンの抽出
            restrictions = extract_restriction_icons(line)
            
            # 説明文からメタ情報を抽出
            related_pages = extract_wikidot_links(description_raw)
            related_tags = extract_related_tags(description_raw)
            target_page_types = extract_target_page_types(description_raw)
            footnotes = extract_footnotes(description_raw)
            other_notes = extract_other_notes(description_raw)
            
            # プレーンテキストの生成
            description_plain = strip_wikidot_syntax(description_raw)
            
            # カテゴリパスの構築
            category_path = build_category_path(current_category, category_stack)
            
            # タグデータの作成
            tag_data = EnhancedTagData(
                slug=tag_slug,
                name_jp=tag_name,
                name_en=tag_en,
                description_raw=description_raw,
                description_plain=description_plain,
                category_path=category_path,
                restrictions=restrictions,
                meta=TagMeta(
                    related_pages=related_pages,
                    related_tags=related_tags,
                    target_page_types=target_page_types,
                    footnotes=footnotes,
                    other_notes=other_notes
                ),
                source_location=SourceLocation(
                    file=current_source_file,
                    line=line_num
                )
            )
            
            tags_data.append(tag_data)
            continue

    safe_print(
        f"DEBUG: Parsing complete. Found {section_count} sections and {tag_count} tags."
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
    parse_jp_tag_list_enhanced()


if __name__ == "__main__":
    main()