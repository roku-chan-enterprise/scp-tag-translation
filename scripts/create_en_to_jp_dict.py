import ast
import json
import os
from typing import Any, cast


def check_tag_consistency() -> None:
    """
    テストケース・en_tags.json・en_to_jp.json のタグ整合性を検証する。
    """
    # 1. テストケースのタグ一覧を取得
    test_py_path = os.path.join(
        os.path.dirname(__file__), "..", "tests", "test_translation.py"
    )
    with open(test_py_path, "r", encoding="utf-8") as f:
        test_py_code = f.read()
    # test_translation_of_specific_tags の test_cases 辞書をASTで抽出
    test_cases_dict: dict[str, Any] | None = None

    class TestCaseVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            if node.name == "test_translation_of_specific_tags":
                for n in ast.walk(node):
                    if isinstance(n, ast.Assign):
                        for t in n.targets:
                            if isinstance(t, ast.Name) and t.id == "test_cases":
                                nonlocal test_cases_dict
                                test_cases_dict = ast.literal_eval(n.value)

    TestCaseVisitor().visit(ast.parse(test_py_code))
    if test_cases_dict is None:
        print(
            "[整合性チェック] test_cases 辞書が test_translation.py から抽出できませんでした"
        )
        test_tags_set: set[str] = set()
    else:
        test_tags_set: set[str] = set(str(k) for k in test_cases_dict.keys())

    # 2. en_tags.json のタグ一覧
    with open("en_tags.json", "r", encoding="utf-8") as f:
        en_tags_data = json.load(f)
    en_tags_set: set[str] = set()
    for item in en_tags_data:
        if isinstance(item, dict) and "name" in item:
            name = cast(str, item["name"])
            en_tags_set.add(name)

    # 3. 辞書のタグ一覧
    dict_path = "dictionaries/en_to_jp.json"
    if os.path.exists(dict_path):
        with open(dict_path, "r", encoding="utf-8") as f:
            dict_data = json.load(f)
        dict_tags_set: set[str] = set(str(k) for k in dict_data.keys())
    else:
        dict_tags_set: set[str] = set()

    # 4. 差分チェック
    missing_in_en_tags: set[str] = test_tags_set - en_tags_set
    missing_in_dict: set[str] = en_tags_set - dict_tags_set
    missing_in_dict_from_test: set[str] = test_tags_set - dict_tags_set

    if missing_in_en_tags:
        print(
            f"[整合性チェック] テストケースにあるが en_tags.json に無いタグ: {missing_in_en_tags}"
        )
    if missing_in_dict:
        print(
            f"[整合性チェック] en_tags.json にあるが dictionaries/en_to_jp.json に無いタグ: {missing_in_dict}"
        )
    if missing_in_dict_from_test:
        print(
            f"[整合性チェック] テストケースにあるが dictionaries/en_to_jp.json に無いタグ: {missing_in_dict_from_test}"
        )
    if not (missing_in_en_tags or missing_in_dict or missing_in_dict_from_test):
        print(
            "[整合性チェック] テストケース・en_tags.json・en_to_jp.json のタグは全て整合しています"
        )


# スクリプトの最初で必ず実行
check_tag_consistency()

# Define file paths
en_tags_path = "en_tags.json"
jp_tags_path = "jp_tags.json"
output_path = "dictionaries/en_to_jp.json"

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Read the JSON files
try:
    en_tags_data: list[dict[str, Any]]  # 型アノテーションを追加
    with open(en_tags_path, "r", encoding="utf-8") as f:
        en_tags_data = json.load(f)
    with open(jp_tags_path, "r", encoding="utf-8") as f:
        jp_tags_data = json.load(f)
except FileNotFoundError as e:
    print(f"Error: Input file not found - {e}")
    exit()
except json.JSONDecodeError as e:
    print(f"Error: Could not decode JSON from input file - {e}")
    exit()

# Create the English to Japanese mapping dictionary
en_to_jp_dict: dict[str, Any] = {}

# Create a dictionary for quick lookup of Japanese tags by their English name
jp_tags_lookup: dict[str, Any] = {
    str(tag.get("name_en")): tag.get("slug")
    for tag in jp_tags_data
    if tag.get("name_en")
}

for en_tag in en_tags_data:
    en_name = en_tag.get("name")
    if en_name:
        jp_slug = jp_tags_lookup.get(str(en_name))
        en_to_jp_dict[str(en_name)] = jp_slug

# Write the output dictionary to a JSON file
try:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(en_to_jp_dict, f, indent=2, ensure_ascii=False)
    print(f"Successfully created {output_path}")
except IOError as e:
    print(f"Error: Could not write to output file - {e}")
