import json
import os
from typing import Any


# Define file paths
en_tags_path = os.path.join("data", "processed", "en_tags.json")
jp_tags_path = os.path.join("data", "processed", "jp_tags.json")
output_path = os.path.join("dictionaries", "en_to_jp.json")

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
