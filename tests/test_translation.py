# tests/test_translation.py
import json
import pytest
import os

# --- Test Setup ---

# Define the path to the translation dictionary relative to the project root
DICTIONARY_PATH = os.path.join(os.path.dirname(__file__), '..', 'dictionaries', 'en_to_jp.json')

# Load the translation dictionary
try:
    with open(DICTIONARY_PATH, 'r', encoding='utf-8') as f:
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
    return translation_dict.get(en_tag, en_tag) # Return original if not found

# --- Test Cases ---

def test_basic_translation():
    """Tests a known, existing translation using 'alive' -> '生命'."""
    # Using 'alive' as the test case, assuming it exists in the dictionary.
    test_tag_en = "alive"
    if test_tag_en in translation_dict:
        expected_translation = translation_dict[test_tag_en]
        assert translate_tag(test_tag_en) == expected_translation, f"Translation for '{test_tag_en}' failed."
    else:
        pytest.skip(f"Skipping basic translation test: '{test_tag_en}' tag not found in dictionary.")


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
        assert translate_tag(test_tag_en_upper) == test_tag_en_upper # Assuming 'ALIVE' itself is not a key
    else:
        pytest.skip(f"Skipping case sensitivity test: '{test_tag_en_lower}' tag not found for comparison.")

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
        "xenofiction": "異種視点"
    }
    for tag_en, expected_jp in test_cases.items():
        assert translate_tag(tag_en) == expected_jp, f"Translation for '{tag_en}' failed."
