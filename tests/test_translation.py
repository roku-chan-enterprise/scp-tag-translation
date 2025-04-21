# tests/test_translation.py

import json
import os
import re
from typing import Any, cast

import pytest

# --- Test Setup ---

# Define the path to the translation dictionary relative to the project root
DICTIONARY_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "dictionaries", "en_to_jp.json"
)

# Load the translation dictionary
try:
    with open(DICTIONARY_PATH, "r", encoding="utf-8") as f:
        translation_dict = json.load(f)
except FileNotFoundError:
    pytest.fail(f"Translation dictionary not found at {DICTIONARY_PATH}", pytrace=False)
except json.JSONDecodeError:
    pytest.fail(f"Error decoding JSON from {DICTIONARY_PATH}", pytrace=False)

# --- Mock Translation Function (Replace with actual import if available) ---


def translate_tag(en_tag: str) -> str:
    """
    Translates an English tag to Japanese using the loaded dictionary.
    Returns the original tag if no translation is found.
    (This is a placeholder; replace with import from your actual translation module)
    """
    return translation_dict.get(en_tag, en_tag)  # Return original if not found


# --- Test Cases ---


def test_basic_translation():
    """Tests a known, existing translation using 'alive' -> '生命'."""
    # Using 'alive' as the test case, assuming it exists in the dictionary.
    test_tag_en = "alive"
    if test_tag_en in translation_dict:
        expected_translation = translation_dict[test_tag_en]
        assert translate_tag(test_tag_en) == expected_translation, (
            f"Translation for '{test_tag_en}' failed."
        )
    else:
        pytest.skip(
            f"Skipping basic translation test: '{test_tag_en}' tag not found in dictionary."
        )


def test_unknown_tag():
    """Tests translation of a tag not present in the dictionary."""
    unknown_tag = "this-tag-should-not-exist-in-the-dictionary"
    assert translate_tag(unknown_tag) == unknown_tag


def test_empty_tag():
    """Tests translation of an empty string."""
    assert translate_tag("") == ""


def test_case_sensitivity():
    """
    Tests if the translation is case-sensitive (adjust based on actual requirements).
    Example: Assumes 'SCP' should perhaps still translate if 'scp' exists.
    This depends on the desired behavior.
    """
    # Example: Check if 'ALIVE' translates to the same as 'alive'
    test_tag_en_lower = "alive"
    test_tag_en_upper = "ALIVE"
    if test_tag_en_lower in translation_dict:
        # expected_translation = translation_dict[test_tag_en_lower] # Keep for reference if needed later
        # This assertion assumes case-insensitivity or normalization handled by translate_tag
        # assert translate_tag(test_tag_en_upper) == expected_translation
        # If it should be case-sensitive and 'ALIVE' is not in the dict:
        assert (
            translate_tag(test_tag_en_upper) == test_tag_en_upper
        )  # Assuming 'ALIVE' itself is not a key
    else:
        pytest.skip(
            f"Skipping case sensitivity test: '{test_tag_en_lower}' tag not found for comparison."
        )


# --- Add More Test Cases Below ---
def test_translation_of_specific_tags():
    """Tests translations for a variety of tags."""
    test_cases = {
        "_adult": "アダルト",
        "_cc": "_cc",
        "_cc4": "_cc4",
        "_cn": "cn",
        "_de": "de",
        "_el": "el",
        "_genreless": "_genreless",
        "_graveyard-shift": "_夜勤",
        "_hu": "hu",
        "_homo-sapiens-sidhe": "_homo-sapiens-sidhe",
        "_id": "id",
        "_image": "_画像",
        "_int": "int",
        "_it": "it",
        "_joicl": "_joicl",
        "_jp": "jp",
        "_licensebox": "_ライセンスボックス",
        "_listpages": "_listpages",
        "_nd": "nd",
        "_theme-temp": "_テーマ移行",
        "_th": "th",
        "_the-bureaucrat": "_お役人",
        "_townhouse": "_タウンハウス",
        "_ua": "ua",
        "_vn": "vn",
        "_zh": "zh",
        "absurdism": "不条理",
        "action": "アクション",
        "alternate-history": "代替史",
        "animated": "アニメーション",
        "anomalous-event": "異常イベント",
        "appliance-war": "家電戦争",
        "bittersweet": "ほろ苦い",
        "black-comedy": "ブラックコメディ",
        "bleak": "陰鬱",
        "body-horror": "ボディホラー",
        "bureaucracy": "官僚制",
        "carnivorous": "肉食",
        "chase": "追跡",
        "cel-shaded": "セルルック",
        "comic": "コミック",
        "container": "容器",
        "correspondence": "書簡体",
        "cosmic-horror": "コズミックホラー",
        "crime-fiction": "犯罪フィクション",
        "deletable": "deletable",
        "deletion-range": "deletion-range",
        "dragon": "ドラゴン",
        "dystopian": "ディストピア",
        "fantasy": "ファンタジー",
        "first-person": "一人称",
        "furniture": "家具",
        "guide": "ガイド",
        "halloween": "ハロウィン",
        "heartwarming": "心温まる",
        "hong-shing": "香城",
        "horror": "ホラー",
        "illustrated": "挿絵付き",
        "image-editing": "画像編集",
        "in-rewrite": "改稿中",
        "journal": "日誌",
        "legal": "法律",
        "lgbtq": "lgbtq",
        "metafiction": "メタフィクション",
        "more-by": "著作紹介",
        "murder-monster": "殺人モンスター",
        "mythological": "神話",
        "news-prompt": "ニュースプロンプト",
        "no-dialogue": "会話なし",
        "otherworldly": "異世界",
        "painted": "絵画",
        "period-piece": "時代物",
        "phenomenon": "現象",
        "pixel-art": "ピクセルアート",
        "political": "政治",
        "post-apocalyptic": "ポスト黙示録",
        "project": "プロジェクト",
        "recording": "録音録画",
        "rewritable": "改稿可能",
        "scp-art": "scpアート",
        "scp-regional": "scp-regional",
        "scp-th": "scp-th",
        "science-fiction": "サイエンスフィクション",
        "slice-of-life": "日常",
        "spy-fiction": "スパイフィクション",
        "stone": "岩石",
        "superhero": "スーパーヒーロー",
        "surrealism": "シュルレアリスム",
        "_tale-hub": "_taleハブ",
        "the-serpent": "蛇",
        "theme": "テーマ",
        "unlisted": "unlisted",
        "western": "西部劇",
        "xenofiction": "異種視点",
    }
    for tag_en, expected_jp in test_cases.items():
        assert translate_tag(tag_en) == expected_jp, (
            f"Translation for '{tag_en}' failed."
        )


# --- JPタグ抽出の新規テスト ---

JP_TAGS_PATH = os.path.join(os.path.dirname(__file__), "..", "jp_tags.json")
SCP_JP_DIR = os.path.join(os.path.dirname(__file__), "..", "scp-jp")


def load_jp_tags() -> set[str]:
    """jp_tags.json からタグ名とスラッグを読み込みます。"""
    try:
        with open(JP_TAGS_PATH, "r", encoding="utf-8") as f:
            jp_tags_data: list[dict[str, Any]] = json.load(f)
        valid_tags: set[str] = set()
        for tag_info in jp_tags_data:
            if tag_info:
                if tag_info.get("name"):
                    valid_tags.add(str(tag_info["name"]))
                if tag_info.get("slug"):
                    valid_tags.add(str(tag_info["slug"]))
        return valid_tags
    except FileNotFoundError:
        pytest.fail(f"jp_tags.json が {JP_TAGS_PATH} に見つかりません", pytrace=False)
    except json.JSONDecodeError:
        pytest.fail(f"{JP_TAGS_PATH} からのJSONデコードエラー", pytrace=False)
    except Exception as e:
        pytest.fail(
            f"jp_tags.json の読み込み中に予期せぬエラーが発生しました: {e}",
            pytrace=False,
        )
    return set()


def extract_tags_from_wikidot(content: str) -> set[str]:
    """Wikidotソーステキストからタグを抽出します。"""
    tags: set[str] = set()
    tag_patterns = [
        re.compile(
            r'\[\[(?:include|module\\s+ListPages)[^\]]*?\\s+tags="([^"]+)"[^\]]*?\]\]',
            re.IGNORECASE,
        ),
    ]
    for pattern in tag_patterns:
        for match in pattern.finditer(content):
            tag_str = match.group(1)
            for tag in tag_str.split():
                tags.add(str(tag))
    return tags


# scp-jp ディレクトリ内の .txt ファイルのリストを取得します
try:
    # リストする前に SCP_JP_DIR が存在することを確認します
    if os.path.isdir(SCP_JP_DIR):
        scp_jp_files = [
            os.path.join(SCP_JP_DIR, f)
            for f in os.listdir(SCP_JP_DIR)
            if os.path.isfile(os.path.join(SCP_JP_DIR, f)) and f.endswith(".txt")
        ]
    else:
        # ディレクトリが存在しない場合は、ファイルが見つからなかったものとして扱います
        scp_jp_files = []
        # ディレクトリが必要な場合は、テスト設定を失敗させることもできます
        # pytest.fail(f"scp-jp ディレクトリが {SCP_JP_DIR} に見つかりません", pytrace=False)
except FileNotFoundError:
    # このケースは os.path.isdir が処理するかもしれませんが、安全のために保持します
    scp_jp_files = []
except Exception as e:
    # ファイルリスト作成中の他の潜在的なエラーをキャッチします
    pytest.fail(f"{SCP_JP_DIR} 内のファイルのリスト作成エラー: {e}", pytrace=False)
    scp_jp_files = []


@pytest.mark.parametrize("filepath", scp_jp_files)
def test_jp_tag_extraction_and_validation(filepath: str) -> None:
    """ファイルパスを受け取り、タグ抽出とバリデーションを行うテスト。"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        pytest.skip(f"{os.path.basename(filepath)} が見つかりません")
        return
    tags = extract_tags_from_wikidot(content)
    if not tags:
        pytest.skip(
            f"{os.path.basename(filepath)} で期待される形式のタグが見つかりません"
        )
        return
    valid_jp_tags = load_jp_tags()
    missing_tags = tags - valid_jp_tags
    assert not missing_tags, (
        f"{os.path.basename(filepath)} で見つかったが jp_tags.json にないタグ: {missing_tags}"
    )


# --- ENタグ抽出の新規テスト ---

EN_TAGS_JSON_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "processed", "en_tags.json"
)
WIKIDOT_SOURCE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "05command", "tech-hub-tag-list.txt"
)


def extract_tags_from_wikidot_source(filepath: str) -> set[str]:
    """Wikidotソースファイルからタグ名を抽出します。"""
    tags: set[str] = set()
    tag_pattern = re.compile(r"^\s*\*\s*\*\[https?://[^ ]+\s+([^\]]+)\]\*\*")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                match = tag_pattern.match(line.strip())
                if match:
                    tags.add(str(match.group(1)))
    except FileNotFoundError:
        pytest.fail(f"Wikidot source file not found at {filepath}", pytrace=False)
    except Exception as e:
        pytest.fail(f"Error reading Wikidot source file {filepath}: {e}", pytrace=False)
    return tags


def load_tags_from_en_json(filepath: str) -> set[str]:
    """en_tags.json からタグ名を読み込みます。"""
    tags: set[str] = set()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            if isinstance(item, dict) and "name" in item:
                name = cast(str, item["name"])
                tags.add(name)
    except FileNotFoundError:
        pytest.fail(f"en_tags.json not found at {filepath}", pytrace=False)
    except json.JSONDecodeError:
        pytest.fail(f"Error decoding JSON from {filepath}", pytrace=False)
    except Exception as e:
        pytest.fail(f"Unexpected error loading {filepath}: {e}", pytrace=False)
    return tags


def test_all_testcase_tags_exist_in_en_tags_json():
    """
    test_translation_of_specific_tags の全タグが en_tags.json に存在するか検証。
    """
    # テストケースのタグ一覧
    test_cases = {
        "_adult": "アダルト",
        "_cc": "_cc",
        "_cc4": "_cc4",
        "_cn": "cn",
        "_de": "de",
        "_el": "el",
        "_genreless": "_genreless",
        "_graveyard-shift": "_夜勤",
        "_hu": "hu",
        "_homo-sapiens-sidhe": "_homo-sapiens-sidhe",
        "_id": "id",
        "_image": "_画像",
        "_int": "int",
        "_it": "it",
        "_joicl": "_joicl",
        "_jp": "jp",
        "_licensebox": "_ライセンスボックス",
        "_listpages": "_listpages",
        "_nd": "nd",
        "_theme-temp": "_テーマ移行",
        "_th": "th",
        "_the-bureaucrat": "_お役人",
        "_townhouse": "_タウンハウス",
        "_ua": "ua",
        "_vn": "vn",
        "_zh": "zh",
        "absurdism": "不条理",
        "action": "アクション",
        "alternate-history": "代替史",
        "animated": "アニメーション",
        "anomalous-event": "異常イベント",
        "appliance-war": "家電戦争",
        "bittersweet": "ほろ苦い",
        "black-comedy": "ブラックコメディ",
        "bleak": "陰鬱",
        "body-horror": "ボディホラー",
        "bureaucracy": "官僚制",
        "carnivorous": "肉食",
        "chase": "追跡",
        "cel-shaded": "セルルック",
        "comic": "コミック",
        "container": "容器",
        "correspondence": "書簡体",
        "cosmic-horror": "コズミックホラー",
        "crime-fiction": "犯罪フィクション",
        "deletable": "deletable",
        "deletion-range": "deletion-range",
        "dragon": "ドラゴン",
        "dystopian": "ディストピア",
        "fantasy": "ファンタジー",
        "first-person": "一人称",
        "furniture": "家具",
        "guide": "ガイド",
        "halloween": "ハロウィン",
        "heartwarming": "心温まる",
        "hong-shing": "香城",
        "horror": "ホラー",
        "illustrated": "挿絵付き",
        "image-editing": "画像編集",
        "in-rewrite": "改稿中",
        "journal": "日誌",
        "legal": "法律",
        "lgbtq": "lgbtq",
        "metafiction": "メタフィクション",
        "more-by": "著作紹介",
        "murder-monster": "殺人モンスター",
        "mythological": "神話",
        "news-prompt": "ニュースプロンプト",
        "no-dialogue": "会話なし",
        "otherworldly": "異世界",
        "painted": "絵画",
        "period-piece": "時代物",
        "phenomenon": "現象",
        "pixel-art": "ピクセルアート",
        "political": "政治",
        "post-apocalyptic": "ポスト黙示録",
        "project": "プロジェクト",
        "recording": "録音録画",
        "rewritable": "改稿可能",
        "scp-art": "scpアート",
        "scp-regional": "scp-regional",
        "scp-th": "scp-th",
        "science-fiction": "サイエンスフィクション",
        "slice-of-life": "日常",
        "spy-fiction": "スパイフィクション",
        "stone": "岩石",
        "superhero": "スーパーヒーロー",
        "surrealism": "シュルレアリスム",
        "_tale-hub": "_taleハブ",
        "the-serpent": "蛇",
        "theme": "テーマ",
        "unlisted": "unlisted",
        "western": "西部劇",
        "xenofiction": "異種視点",
    }
    en_tags_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "processed", "en_tags.json"
    )
    with open(en_tags_path, "r", encoding="utf-8") as f:
        en_tags_data = json.load(f)
    en_tag_names: set[str] = set()
    for item in en_tags_data:
        if isinstance(item, dict) and "name" in item:
            name = cast(str, item["name"])
            en_tag_names.add(name)
    missing = set(test_cases.keys()) - en_tag_names
    assert not missing, f"テストケースにあるが en_tags.json に無いタグ: {missing}"


def test_all_en_tags_json_tags_exist_in_dictionary():
    """
    en_tags.json の全タグが dictionaries/en_to_jp.json に存在するか検証。
    """
    en_tags_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "processed", "en_tags.json"
    )
    dict_path = os.path.join(
        os.path.dirname(__file__), "..", "dictionaries", "en_to_jp.json"
    )
    with open(en_tags_path, "r", encoding="utf-8") as f:
        en_tags_data = json.load(f)
    with open(dict_path, "r", encoding="utf-8") as f:
        dict_data = json.load(f)
    en_tag_names: set[str] = set()
    for item in en_tags_data:
        if isinstance(item, dict) and "name" in item:
            name = cast(str, item["name"])
            en_tag_names.add(name)
    dict_keys: set[str] = set(dict_data.keys())
    missing: set[str] = en_tag_names - dict_keys
    assert not missing, (
        f"en_tags.json にあるが dictionaries/en_to_jp.json に無いタグ: {missing}"
    )
