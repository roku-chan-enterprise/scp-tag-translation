# tests/test_translation.py

import json
import os
import re
from typing import Any, cast

import pytest

# --- Test Setup ---

# Define the path to the translation dictionary relative to the project root
DICTIONARY_PATH = os.path.join(
    os.path.dirname(__file__), "..", "dictionaries", "en_to_jp.json"
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
    # Return original tag if translation is None in the dictionary
    return translation_dict.get(en_tag, en_tag) if translation_dict.get(en_tag) is not None else None


# --- Test Cases ---


def test_basic_translation():
    """Tests a known, existing translation using 'alive' -> '生命'."""
    # Using 'alive' as the test case, assuming it exists in the dictionary.
    test_tag_en = "alive"
    if test_tag_en in translation_dict and translation_dict[test_tag_en] is not None:
        expected_translation = translation_dict[test_tag_en]
        assert translate_tag(test_tag_en) == expected_translation, (
            f"Translation for '{test_tag_en}' failed."
        )
    else:
        pytest.skip(
            f"Skipping basic translation test: '{test_tag_en}' tag not found or has null translation in dictionary."
        )


def test_unknown_tag():
    """Tests translation of a tag not present in the dictionary."""
    unknown_tag = "this-tag-should-not-exist-in-the-dictionary"
    assert translate_tag(unknown_tag) is None


def test_empty_tag():
    """Tests translation of an empty string."""
    assert translate_tag("") is None


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
            translate_tag(test_tag_en_upper) is None
        )  # Assuming 'ALIVE' itself is not a key
    else:
        pytest.skip(
            f"Skipping case sensitivity test: '{test_tag_en_lower}' tag not found for comparison."
        )


# --- Add More Test Cases Below ---
def test_translation_of_specific_tags():
    """Tests translations for a variety of tags."""
    test_cases = {
        "scp": "scp",
        "goi-format": "goi-format",
        "tale": "tale",
        "supplement": "補足",
        "site": "サイト",
        "essay": "エッセイ",
        "news": "ニュース",
        "resource": "資料",
        "author": "著者ページ",
        "artist": "アーティスト",
        "artwork": "アートワーク",
        "component": "コンポーネント",
        "component-backend": "コンポーネント・バックエンド",
        "theme": "テーマ",
        "fragment": "フラグメント",
        "more-by": "著作紹介",
        "forum": "フォーラム",
        "splash": "見出し",
        "redirect": "リダイレクト",
        "admin": "管理",
        "hub": "ハブ",
        "workbench": "ワークベンチ",
        "sandbox": "サンドボックス",
        "001-proposal": "001提言",
        "archived": "アーカイブ済み",
        "co-authored": "共著",
        "collaboration": "合作",
        "contest": "コンテスト",
        "joke": "ジョーク",
        "poetry": "詩的文学",
        "required": "必読",
        "_tale-hub": "_taleハブ",
        "safe": "safe",
        "euclid": "euclid",
        "keter": "keter",
        "thaumiel": "thaumiel",
        "apollyon": "apollyon",
        "archon": "archon",
        "ticonderoga": "ticonderoga",
        "neutralized": "neutralized",
        "decommissioned": "decommissioned",
        "pending": "pending",
        "esoteric-class": "esoteric-class",
        "adaptive": "適応",
        "alive": "生命",
        "amorphous": "不定形",
        "autonomous": "自律",
        "bacteria": "バクテリア",
        "clown": "道化師",
        "fungus": "真菌類",
        "hive-mind": "集団意識",
        "hostile": "敵対的",
        "humanoid": "人間型",
        "metamorphic": "変身",
        "predatory": "捕食",
        "plant": "植物",
        "sapient": "知性",
        "species": "種族",
        "swarm": "群れ",
        "virus": "ウイルス",
        "animal": "動物",
        "amphibian": "両生類",
        "arachnid": "クモ",
        "arthropod": "節足動物",
        "bear": "クマ",
        "bee": "ハチ",
        "bird": "鳥類",
        "bovine": "ウシ",
        "butterfly": "チョウ",
        "canine": "イヌ",
        "cephalopod": "頭足類",
        "cetacean": "クジラ",
        "crustacean": "甲殻類",
        "deer": "シカ",
        "dinosaur": "恐竜",
        "equine": "ウマ",
        "feline": "ネコ",
        "fish": "魚類",
        "insect": "昆虫",
        "invertebrate": "無脊椎動物",
        "primate": "サル",
        "rabbit": "ウサギ",
        "reptile": "爬虫類",
        "rodent": "齧歯類",
        "shark": "軟骨魚類",
        "snake": "ヘビ",
        "worm": "ワーム",
        "biological": "生物学",
        "biohazard": "生物災害",
        "blood": "血液",
        "cadaver": "死体",
        "contagion": "伝染性",
        "dental": "歯",
        "extremity": "体肢",
        "genetic": "遺伝子",
        "medical": "医療",
        "nocturnal": "夜行性",
        "ocular": "眼",
        "parasitic": "寄生",
        "reanimation": "蘇生",
        "reproductive": "生殖",
        "sexual": "性的",
        "skeletal": "骨格",
        "toxic": "毒性",
        "addictive": "中毒",
        "antimemetic": "反ミーム",
        "auditory": "聴覚",
        "cognitohazard": "認識災害",
        "compulsion": "強制力",
        "empathic": "精神感応",
        "gustatory": "味覚",
        "hallucination": "幻覚",
        "infohazard": "情報災害",
        "knowledge": "知識",
        "language": "言語",
        "memetic": "ミーム",
        "mimetic": "擬態",
        "memory-affecting": "記憶影響",
        "mind-affecting": "精神影響",
        "neurological": "神経",
        "observational": "観測",
        "olfactory": "嗅覚",
        "predictive": "予知",
        "sensory": "感覚",
        "sleep": "睡眠",
        "tactile": "触覚",
        "telepathic": "テレパシー",
        "visual": "視覚",
        "acoustic": "音波",
        "chemical": "化学",
        "corrosive": "腐食",
        "ectoentropic": "外部エントロピー",
        "electrical": "電気",
        "electromagnetic": "電磁気",
        "entropic": "エントロピー",
        "fire": "炎",
        "gaseous": "気体",
        "gravity": "重力",
        "immobile": "移動不可能",
        "indestructible": "破壊不可能",
        "intangible": "非実体",
        "light": "可視光",
        "liquid": "液体",
        "magnetic": "磁力",
        "meteorological": "天候",
        "microscopic": "微視的",
        "miniature": "ミニチュア",
        "mobile": "移動",
        "portal": "ポータル",
        "paradox": "パラドックス",
        "polyhedral": "多面体",
        "radioactive": "放射能",
        "reality-bending": "現実改変",
        "self-repairing": "自己修復",
        "self-replicating": "自己複製",
        "shadow": "影",
        "spatial": "空間",
        "sphere": "球体",
        "telekinetic": "念力",
        "teleportation": "瞬間移動",
        "temporal": "時間",
        "thaumaturgy": "奇跡術",
        "thermal": "温度",
        "thermodynamic": "熱力学",
        "transfiguration": "変容",
        "transmission": "通信",
        "vibration": "振動",
        "appliance": "家電",
        "artistic": "芸術",
        "artifact": "人工",
        "clockwork": "ぜんまい仕掛け",
        "clothing": "衣類",
        "cinema": "映画",
        "computer": "コンピュータ",
        "currency": "貨幣",
        "document": "文書",
        "electronic": "電子デバイス",
        "food": "食物",
        "inscription": "記述",
        "jewelry": "装飾品",
        "mechanical": "機械",
        "media": "記憶媒体",
        "musical": "音楽",
        "online": "オンライン",
        "performance": "芸能",
        "photographic": "写真",
        "robotic": "自動装置",
        "sculpture": "彫像",
        "tool": "道具",
        "toy": "玩具",
        "weapon": "武器",
        "vehicle": "乗り物",
        "airborne": "空中",
        "aquatic": "水中",
        "building": "建造物",
        "city": "都市",
        "extradimensional": "異次元",
        "extraterrestrial": "地球外",
        "forest": "森林",
        "geological": "地質",
        "island": "島嶼",
        "library": "図書館",
        "location": "場所",
        "moon": "月",
        "planet": "惑星",
        "satellite": "衛星",
        "structure": "構造",
        "subterranean": "地下",
        "sun": "太陽",
        "concept": "概念",
        "exchange": "交換",
        "foundation-made": "財団製",
        "future": "未来",
        "game": "ゲーム",
        "k-class-scenario": "k-クラスシナリオ",
        "loop": "ループ",
        "mathematical": "数学",
        "military": "軍事",
        "meta": "メタ",
        "narrative": "語り",
        "probability": "確率",
        "religious": "宗教",
        "ritual": "儀式",
        "sport": "スポーツ",
        "uncontained": "未収容",
        "ghost": "霊体",
        "historical": "歴史",
        "afterlife": "死後",
        "corporate": "企業",
        "orientation": "orientation",
        "abnormalities": "怪奇部門",
        "angle-grinders": "角度研削者",
        "antimemetics-division": "反ミーム部門",
        "decommissioning-dept": "解体部門",
        "deletions-dept": "削除部門",
        "delta-t": "デルタ-t",
        "ethics-committee": "倫理委員会",
        "ettra": "ettra",
        "fire-suppression-dept": "火急鎮静部門",
        "folklore-dept": "神話・民俗学部門",
        "last-hope": "残された希望",
        "miscommunications": "誤伝達部門",
        "department-of-other": "番外部門",
        "pataphysics-dept": "空想科学部門",
        "procurement-liquidation-dept": "調達・清算部門",
        "surrealistics-dept": "超現実部門",
        "tactical-theology": "戦術神学部門",
        "samsara": "サムサラ",
        "telecom-office": "電気通信監視室",
        "unreality-dept": "非現実部門",
        "accelerate-the-future": "accelerate-the-future",
        "alexylva": "alexylva大学",
        "ambrose-restaurant": "アンブローズ・レストラン",
        "anderson": "アンダーソン",
        "arcadia": "アルカディア",
        "are-we-cool-yet": "are-we-cool-yet",
        "asci": "asci",
        "avelar": "アベラール",
        "black-queen": "黒の女王",
        "british-occult-service": "british-occult-service",
        "broken-god": "壊れた神の教会",
        "brothers-of-death": "brothers-of-death",
        "chaos-insurgency": "カオス・インサージェンシー",
        "chicago-spirit": "シカゴ・スピリット",
        "children-of-the-night": "夜闇の子ら",
        "children-of-the-torch": "松明の子供達",
        "class-of-76": "class-of-76",
        "cogwork-orthodoxy": "歯車仕掛正教",
        "daevite": "daevite",
        "deer-college": "ディア大学",
        "dr-wondertainment": "ワンダーテインメント博士",
        "factory": "ファクトリー",
        "fifthist": "第五教会",
        "gamers-against-weed": "ゲーマーズアゲインストウィード",
        "giftschreiber": "ギフトシュライバー",
        "global-occult-coalition": "世界オカルト連合",
        "goldbaker-reinz": "ゴールドベイカー・ラインツ",
        "golden-horde": "金帳汗国",
        "greazeburger": "グリーズバーガー",
        "gru-division-p": "gru-p-部局",
        "herman-fuller": "ハーマン・フラー",
        "hmfscp": "hmfscp",
        "homo-sapiens-sidhe": "homo-sapiens-sidhe",
        "horizon-initiative": "境界線イニシアチブ",
        "hunters-black-lodge": "ハンターの黒きロッジ",
        "ijamea": "ijamea",
        "just-girly-things": "just-girly-things",
        "madao": "madao",
        "mages-academy": "魔術師学会",
        "manna-charitable-foundation": "マナによる慈善財団",
        "marshall-carter-and-dark": "mc&d",
        "maxwellism": "マクスウェリズム",
        "nameless": "名もなきもの",
        "nobody": "何者でもない",
        "obearwatch": "監督真司令部",
        "obskura": "オブスクラ",
        "oneiroi": "オネイロイ",
        "oria": "oria",
        "parawatch": "パラウォッチ",
        "pattern-screamer": "pattern-screamer",
        "pentagram": "ペンタグラム",
        "prometheus": "プロメテウス",
        "sapphire": "saphir",
        "sarkic": "サーキック",
        "scarlet-king": "scarlet-king",
        "second-hytoth": "第二ハイトス教会",
        "serpents-hand": "蛇の手",
        "shark-punching-center": "サメ殴りセンター",
        "silicon-nornir": "silicon-nornir",
        "sugarcomb-confectionery": "シュガーコム製菓",
        "three-moons-initiative": "三ツ月イニシアチブ",
        "totleighsoft": "トトレイソフト",
        "unusual-incidents-unit": "異常事件課",
        "valravn": "ヴァルラウン",
        "vikander-kneed": "ヴィキャンデル・ニード",
        "wandsmen": "堂守連盟",
        "westhead-media": "ウェストヘッド・メディア",
        "world-parahealth-organization": "世界超保健機関",
        "wilsons-wildlife": "ウィルソンズ・ワイルドライフ",
        "xia-dynasty": "夏王朝",
        "_alexylva": "_alexylva大学",
        "_ambrose-restaurant": "_アンブローズ・レストラン",
        "_anderson": "_アンダーソン",
        "_arcadia": "_アルカディア",
        "_are-we-cool-yet": "_are-we-cool-yet",
        "_black-queen": "_黒の女王",
        "_broken-god": "_壊れた神の教会",
        "_chaos-insurgency": "_カオス・インサージェンシー",
        "_chicago-spirit": "_シカゴ・スピリット",
        "_deer-college": "_ディア大学",
        "_eric": "_エリック",
        "_factory": "_ファクトリー",
        "_fifthist": "_第五教会",
        "_global-occult-coalition": "_世界オカルト連合",
        "_gru-division-p": "_gru-p-部局",
        "_herman-fuller": "_ハーマン・フラー",
        "_horizon-initiative": "_境界線イニシアチブ",
        "_icsut": "_icsut",
        "_ijamea": "_ijamea",
        "_la-rue-macabre": "_ラ・リュー・マカーブラー",
        "_madao": "_madao",
        "_manna-charitable-foundation": "_マナによる慈善財団",
        "_marshall-carter-and-dark": "_mc&d",
        "_nobody": "_何者でもない",
        "_oneiroi": "_オネイロイ",
        "_oria": "_oria",
        "_other": "_その他団体-en",
        "_parawatch": "_パラウォッチ",
        "_prometheus": "_プロメテウス",
        "_sarkic": "_サーキック",
        "_second-hytoth": "_第二ハイトス教会",
        "_serpents-hand": "_蛇の手",
        "_shark-punching-center": "_サメ殴りセンター",
        "_three-moons-initiative": "_三ツ月イニシアチブ",
        "_unusual-cargo": "_異常積荷委員会",
        "_unusual-incidents-unit": "_異常事件課",
        "_valravn": "_ヴァルラウン",
        "_wandsmen": "_堂守連盟",
        "_wilsons-wildlife": "_ウィルソンズ・ワイルドライフ",
        "aces-and-eights": "死人の手札",
        "aiad": "aiad",
        "ad-astra": "アド・アストラ",
        "alchemy-department": "錬金術部門",
        "antarctic-exchange": "南極の交流",
        "apotheosis": "アポセオシス",
        "bellerverse": "鐘を鳴らす者の詩",
        "broken-masquerade": "壊された虚構",
        "but-a-dream": "ただの夢",
        "competitive-eschatology": "競り合う終末論",
        "cool-war-2": "クールな戦争2",
        "daybreak": "破暁",
        "doctors-of-the-church": "教会の博士",
        "dread&circuses": "ドレッド&サーカス",
        "end-of-death": "死の終焉",
        "eventyr": "eventyr",
        "from-120s-archives": "120の記録書庫より",
        "green-king": "翠の王",
        "heimdall": "ヘイムダル",
        "insect-hell": "insect-hell",
        "lampeter": "ランピーター",
        "lolfoundation": "たのしいざいだん",
        "man-who-wasnt-there": "存在しなかった者",
        "memoria-adytum": "追憶のアディトゥム",
        "nightfall": "ナイトフォール",
        "ninth-world": "第九世界",
        "no-return": "ノー・リターン",
        "old-man-in-the-sea": "老人との海",
        "on-guard-43": "on-guard-43",
        "on-mount-golgotha": "ゴルゴタの丘で",
        "only-game-in-town": "最上の事",
        "orcadia": "オルカディア",
        "pitch-haven": "pitch-haven",
        "rats-nest": "ラッツネスト",
        "resurrection": "リザレクション",
        "s&c-plastics": "s&cプラスチック",
        "ship-in-a-bottle": "ボトルシップ",
        "simulacrum": "simulacrum",
        "sotm": "sotm",
        "the-coldest-war": "極寒の戦争",
        "the-gulf": "メキシコ湾",
        "the-trashfire": "トラッシュファイア",
        "third-law": "第三法則",
        "twisted-pines": "あのヨレハマツの林",
        "unfounded": "財団のない世界",
        "unhuman": "人ならぬもの",
        "war-on-all-fronts": "全ての戦線で戦え",
        "wonderful-world": "素晴らしき世界",
        "abcs-of-death": "死のabc",
        "admonition": "訓戒",
        "anabasis": "アナバシス",
        "ao-tale": "ao-tale",
        "black-rabbit-company": "ブラックラビット社",
        "cack-hard": "カック・ハード",
        "classical-revival": "classical-revival",
        "collector-tale": "コレクターtale",
        "etdp": "etdp",
        "goc-casefiles": "goc事件簿",
        "harbinger": "ハービンジャー",
        "hecatoncheires-cycle": "ヘカトンケイレス・サイクル",
        "integration-program": "統合プログラム",
        "kiryu-labs": "kiryu-labs",
        "mister": "mister",
        "mundus-liberari": "世界に自由を",
        "old-foes": "旧敵たち",
        "olympia": "olympia",
        "phobia-anthology": "恐怖症アンソロジー",
        "palisade": "防御柵計画",
        "project-crossover": "project-crossover",
        "project-thaumiel": "project-thaumiel",
        "team-bird": "team-bird",
        "time-after-time-password": "タイム・アフター・タイム・パスワード",
        "whore-of-blood": "血の娼婦",
        "yggdrasil-s-surveyor": "ユグドラシルの測量技師",
        "8-ball": "8-ボール",
        "aaron-siegel": "aaron-siegel",
        "agent-adams": "エージェント・アダムス",
        "agent-calendar": "エージェント・カレンダー",
        "agent-green": "エージェント・グリーン",
        "agent-kazmarek": "エージェント・カズマレク",
        "agent-laferrier": "エージェント・ラフェリエール",
        "agent-lament": "エージェント・ラメント",
        "agent-lurk": "エージェント・ラーク",
        "agent-merlo": "エージェント・メルロ",
        "agent-navarro": "エージェント・ナヴァッロ",
        "agent-popescu": "エージェント・ポペスク",
        "agent-rodney": "エージェント・ロドニー",
        "agent-strelnikov": "エージェント・ストレルニコフ",
        "agent-trauss": "エージェント・トラウス",
        "agent-yoric": "エージェント・ヨリック",
        "alexandra": "アレクサンドラ",
        "alex-thorley": "アレックス・ソーリー",
        "chief-ibanez": "イバニェス主任",
        "bailey-brothers": "ベイリー三兄弟",
        "captain-adrian": "キャプテン・エイドリアン",
        "d-7294": "d-7294",
        "d-11424": "d-11424",
        "director-aktus": "アクタス管理官",
        "director-bold": "ボールド管理官",
        "director-bohart": "ボハート管理官",
        "director-diaghilev": "ディアギレフ管理官",
        "director-gillespie": "ガレスピー管理官",
        "director-graham": "グラハム管理官",
        "director-mcinnis": "マッキンス管理官",
        "director-mctiriss": "マックティリス管理官",
        "director-moose": "ムース管理官",
        "director-scout": "スカウト管理官",
        "director-lague": "ラグー管理官",
        "django-bridge": "ジャンゴ・ブリッジ博士",
        "doctor-asheworth": "アシュワース博士",
        "doctor-blank": "ブランク博士",
        "doctor-bright": "ブライト博士",
        "doctor-cimmerian": "シメリアン博士",
        "doctor-clef": "クレフ博士",
        "doctor-dan": "ダン博士",
        "doctor-edison": "エジソン博士",
        "doctor-elliott": "エリオット博士",
        "doctor-elstrom": "エルストロム博士",
        "doctor-everwood": "エバーウッド博士",
        "doctor-gears": "ギアーズ博士",
        "doctor-gerald": "ジェラルド博士",
        "doctor-glass": "グラス博士",
        "doctor-heiden": "doctor-heiden",
        "doctor-hoygull": "ホイガル博士",
        "doctor-iceberg": "アイスバーグ博士",
        "doctor-king": "キング博士",
        "doctor-kondraki": "コンドラキ博士",
        "doctor-light": "ライト博士",
        "doctor-lillihammer": "リリハンメル博士",
        "doctor-mann": "マン博士",
        "doctor-mcdoctorate": "マクドクトラート博士",
        "doctor-reynders": "レインデルス博士",
        "doctor-rights": "ライツ博士",
        "doctor-rivera": "リベラ博士",
        "doctor-roget": "ロジェ博士",
        "doctor-scranton": "スクラントン博士",
        "doctor-sinclair": "シンクレア博士",
        "doctor-sokolsky": "ソコルスキー博士",
        "doctor-sorts": "ソーツ博士",
        "doctor-thereven": "セレヴン博士",
        "doctor-wettle": "ウェトル博士",
        "draven-kondraki": "ドレイヴン・コンドラキ",
        "general-bowe": "バウ将軍",
        "glacon": "グラソン",
        "hadfield-twins": "ハドフィールド家の双子",
        "james-harkness": "ジェームス・ハークネス",
        "judith-low": "ジュディス・ロゥ博士",
        "kain-pathos-crow": "ケイン・パトス・クロウ",
        "lombardi": "ロンバルディ",
        "maria-jones": "マリア・ジョーンズ",
        "marie-surratt": "マリー・サラット",
        "marion-wheeler": "マリオン・ホイーラー",
        "mark-kiryu": "マーク・桐生",
        "odongo-tejani": "オドンゴ・テジャニ",
        "philip-deering": "フィリップ・ディアリング",
        "primrose-esquire": "プリムローズ法務官",
        "professor-bjornsen": "professor-bjornsen",
        "researcher-conwell": "コーンウェル研究員",
        "researcher-james": "ジェームズ研究員",
        "researcher-labelle": "researcher-labelle",
        "researcher-lloyd": "ロイド研究員",
        "researcher-rosen": "ローゼン研究員",
        "researcher-rex": "レックス研究員",
        "researcher-smalls": "スモールズ研究員",
        "researcher-talloran": "タローラン研究員",
        "riven-mercer": "リーヴィン・マーサー",
        "samara-maclear": "サマラ・マクレア",
        "sheldon-katz": "シェルドン・カッツ",
        "simon-pietrykau": "サイモン・ピエトリカウ",
        "thad-xyank": "シャンク博士",
        "the-administrator": "管理者",
        "yossarian-leiner": "yossarian-leiner",
        "zyn-kiryu": "ジン・桐生",
        "able": "アベル",
        "alexei-belitrov": "アレクセイ・ベリトロフ",
        "alleged-god": "scp-343",
        "blackwood": "blackwood",
        "bobble-the-clown": "ピエロのボブル",
        "bones": "bones",
        "cain": "カイン",
        "cousin-johnny": "従兄弟のジョニー",
        "doctor-spanko": "ドクター・スパンコ",
        "donkman": "ドンクマン",
        "fred": "フレッド",
        "geoffrey-quincy-harrison": "ジェフリー・クインシー・ハリソン",
        "grabnok": "グラブノック",
        "half-cat-josie": "半身猫のジョーシー",
        "heather-mason": "ヘザー・メイソン",
        "hogslice": "hogslice",
        "iris-thompson": "アイリス・トンプソン",
        "leslie": "レスリー",
        "marw": "マーウ",
        "moon-champion": "ムーン・チャンピオン",
        "mr-fish": "ミスター・おさかな",
        "murphy-law": "マーフィー・ロゥ",
        "old-ai": "オールドai",
        "plague-doctor": "ペスト医師",
        "possessive-mask": "取り憑くマスク",
        "rainer-miller": "ライナー・ミラー",
        "sauelsuesor": "サウエルスエソル",
        "shy-guy": "シャイガイ",
        "teenage-gaea": "年頃のガイア",
        "ten-dots": "scp-2521",
        "the-old-man": "オールドマン",
        "tickle-monster": "くすぐりオバケ",
        "the-sculpture": "scp-173",
        "the-specter": "the-specter",
        "aldon": "アルドン",
        "big-cheese-horace": "ビッグチーズ・ホレス",
        "brainy-brian": "ブレイニー・ブライアン",
        "chaz-ambrose": "チャズ・アンブローズ",
        "dado": "dado",
        "damien-nowak": "ダミアン・ノヴァク",
        "dc-al-fine": "d.c.アルフィーネ",
        "eric": "エリック",
        "esther-kogan": "エスター・コーガン",
        "faeowynn-wilson": "フェオウィン・ウィルソン",
        "finnegan": "フィネガン",
        "grand-karcist-ion": "崇高なるカルキスト・イオン",
        "halyna-ieva": "ハリーナ・イエヴァ",
        "hanged-king": "吊られた王",
        "holly-light": "ホリィ・ライト",
        "icky": "イッキィ",
        "iris-dark": "アイリス・ダーク",
        "isabel-v": "イザベル五世",
        "jockjamsvol6": "jockjamsvol6",
        "jude-kriyot": "ジュード・クライヨット",
        "judy-papill": "ジュディ・パピル",
        "kenneth-spencer": "ケネス・スペンサー",
        "kindness": "kindness",
        "legate-trunnion": "レガーテ・トラニオン",
        "lewitt-zairi-family": "ルウィット・ザイリ・ファミリー",
        "lovataar": "ロヴァタール",
        "manny": "マニー",
        "mari-macphaerson": "マリ・マクファーソン",
        "midnight-the-cat": "ミッドナイト",
        "nadox": "ナドックス",
        "olivie-gwyneth": "オリヴィエ・ギネス",
        "orok": "オロク",
        "pangloss": "パングロス",
        "polaricecraps": "polaricecraps",
        "professor-aw": "aw教授",
        "queen-mab": "マブ女帝",
        "richard-chappell": "リチャード・チャペル",
        "robert-bumaro": "ロバート・ブマロ",
        "robin-thorne": "ロビン・ソーン",
        "ruiz-duchamp": "ルイス・デュシャン",
        "saarn": "サアルン",
        "saint-hedwig": "聖ヘドウィグ",
        "saturn-deer": "saturn-deer",
        "the-critic": "批評家",
        "the-engineer": "エンジニア",
        "thilo-zwist": "ティロ・ツウィスト",
        "tim-wilson": "ティム・ウィルソン",
        "veronica-fitzroy": "ベロニカ・フィッツロイ",
        "vincent-anderson": "ヴィンセント・アンダーソン",
        "7th-occult-war": "7th-occult-war",
        "alagadda": "アラガッダ",
        "backdoor-soho": "バックドア・ソーホー",
        "deus-ex-machina": "機械仕掛けの神",
        "esterberg": "エスターバーグ",
        "hy-brasil": "ハイ・ブラジル",
        "la-rue-macabre": "ラ・リュー・マカーブラー",
        "three-portlands": "スリー・ポートランド",
        "undervegas": "アンダーベガス",
        "wanderers-library": "放浪者の図書館",
        "audio": "音声添付",
        "interactive": "インタラクティブ",
        "video": "映像添付",
        "in-rewrite": "改稿中",
        "rewritable": "改稿可能",
        "rewrite": "改稿",
        "featured": "注目記事",
        "prize-feature": "賞典-注目記事",
        "reviewers-spotlight": "批評者スポットライト",
        "event-featured": "イベント-注目記事",
        "metadata": "メタデータ",
        "_cc": "_cc",
        "_image": "_画像",
        "_licensebox": "_ライセンスボックス",
        "_theme-temp": "_テーマ移行",
        "173fest": "173fest",
        "art-exchange": "art-exchange",
        "af2014": "af2014",
        "game-day": "game-day",
        "pridefest2024": "pridefest24",
        "spring-cleaning24": "spring-cleaning24",
        "1000": "1000",
        "2000": "2000",
        "3000": "3000",
        "4000": "4000",
        "5000": "5000",
        "6000": "6000",
        "7000": "7000",
        "8000": "8000",
        "gbc09": "gbc09",
        "talecon10": "talecon10",
        "hc2012": "hc2012",
        "nyc2013": "nyc2013",
        "five-questions": "five-questions",
        "tc2013": "tc2013",
        "uac2014": "uac2014",
        "dc2014": "dc2014",
        "goi2014": "goi2014",
        "sc2015": "sc2015",
        "rei2015": "rei2015",
        "af2016": "af2016",
        "mtf2016": "mtf2016",
        "d-con2016": "d-con2016",
        "hiscon2017": "hiscon2017",
        "art2017": "art2017",
        "jam-con2018": "jam-con2018",
        "halloween2018": "halloween2018",
        "doomsday2018": "doomsday2018",
        "jam-con2019": "jam-con2019",
        "cliche2019": "cliche2019",
        "collab-con2019": "collab-con2019",
        "goi2019": "goi2019",
        "jam-con2020": "jam-con2020",
        "exquisite-corpse2020": "exquisite-corpse2020",
        "canon2020": "canon2020",
        "cupid2021": "cupid2021",
        "jam-con2021": "jam-con2021",
        "halloweencon2022": "halloweencon2022",
        "departmentcon2022": "departmentcon2022",
        "coldpostcon": "coldpostcon",
        "remixcon2023": "remixcon2023",
        "lorecon2023": "lorecon2023",
        "visual-archives2024": "visual-archives2024",
        "publicdomaincon2025": "publicdomaincon2025",
        "memecon2021-unofficial": "memecon2021-unofficial",
        "romcon2023-unofficial": "romcon2023-unofficial",
        "spook-nico-2024-unofficial": "spook-nico-2024-unofficial",
        "international": "インターナショナル"
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
        f"テストケースにあるが jp_tags.json にないタグ: {missing_tags}"
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
        "_cc": "_cc",
        "_cc4": None,
        "_cn": None,
        "_de": None,
        "_el": None,
        "_genreless": None,
        "_graveyard-shift": None,
        "_hu": None,
        "_homo-sapiens-sidhe": None,
        "_id": None,
        "_image": "_画像",
        "_int": None,
        "_it": None,
        "_joicl": None,
        "_jp": None,
        "_licensebox": "_ライセンスボックス",
        "_listpages": None,
        "_nd": None,
        "_theme-temp": None,
        "_the-bureaucrat": None,
        "_townhouse": None,
        "_ua": None,
        "_vn": None,
        "_zh": None,
        "absurdism": None,
        "action": None,
        "alternate-history": None,
        "animated": None,
        "anomalous-event": None,
        "appliance-war": None,
        "bittersweet": None,
        "black-comedy": None,
        "bleak": None,
        "body-horror": None,
        "bureaucracy": None,
        "chase": None,
        "cel-shaded": None,
        "comic": None,
        "correspondence": None,
        "cosmic-horror": None,
        "crime-fiction": None,
        "deletable": None,
        "deletion-range": None,
        "dragon": None,
        "dystopian": None,
        "fantasy": None,
        "first-person": None,
        "guide": None,
        "halloween": None,
        "heartwarming": None,
        "hong-shing": None,
        "horror": None,
        "illustrated": None,
        "image-editing": None,
        "in-rewrite": None,
        "journal": None,
        "legal": None,
        "lgbtq": None,
        "metafiction": None,
        "more-by": None,
        "murder-monster": None,
        "mythological": None,
        "news-prompt": None,
        "no-dialogue": None,
        "otherworldly": None,
        "painted": None,
        "period-piece": None,
        "phenomenon": None,
        "pixel-art": None,
        "political": None,
        "post-apocalyptic": None,
        "rewritable": None,
        "scp-art": None,
        "science-fiction": None,
        "slice-of-life": None,
        "spy-fiction": None,
        "superhero": None,
        "surrealism": None,
        "_tale-hub": None,
        "the-serpent": None,
        "theme": None,
        "unlisted": None,
        "western": None,
        "xenofiction": None,
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
        f"テストケースにあるが jp_tags.json にないタグ: {missing_tags}"
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
        "_cc": "_cc",
        "_cc4": None,
        "_cn": None,
        "_de": None,
        "_el": None,
        "_genreless": None,
        "_graveyard-shift": None,
        "_hu": None,
        "_homo-sapiens-sidhe": None,
        "_id": None,
        "_image": "_画像",
        "_int": None,
        "_it": None,
        "_joicl": None,
        "_jp": None,
        "_licensebox": "_ライセンスボックス",
        "_listpages": None,
        "_nd": None,
        "_theme-temp": None,
        "_the-bureaucrat": None,
        "_townhouse": None,
        "_ua": None,
        "_vn": None,
        "_zh": None,
        "absurdism": None,
        "action": None,
        "alternate-history": None,
        "animated": None,
        "anomalous-event": None,
        "appliance-war": None,
        "bittersweet": None,
        "black-comedy": None,
        "bleak": None,
        "body-horror": None,
        "bureaucracy": None,
        "chase": None,
        "cel-shaded": None,
        "comic": None,
        "correspondence": None,
        "cosmic-horror": None,
        "crime-fiction": None,
        "deletable": None,
        "deletion-range": None,
        "dragon": None,
        "dystopian": None,
        "fantasy": None,
        "first-person": None,
        "guide": None,
        "halloween": None,
        "heartwarming": None,
        "hong-shing": None,
        "horror": None,
        "illustrated": None,
        "image-editing": None,
        "in-rewrite": None,
        "journal": None,
        "legal": None,
        "lgbtq": None,
        "metafiction": None,
        "more-by": None,
        "murder-monster": None,
        "mythological": None,
        "news-prompt": None,
        "no-dialogue": None,
        "otherworldly": None,
        "painted": None,
        "period-piece": None,
        "phenomenon": None,
        "pixel-art": None,
        "political": None,
        "post-apocalyptic": None,
        "rewritable": None,
        "scp-art": None,
        "science-fiction": None,
        "slice-of-life": None,
        "spy-fiction": None,
        "superhero": None,
        "surrealism": None,
        "_tale-hub": None,
        "the-serpent": None,
        "theme": None,
        "unlisted": None,
        "western": None,
        "xenofiction": None,
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
