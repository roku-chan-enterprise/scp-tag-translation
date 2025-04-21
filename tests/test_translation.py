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
# Consider:
# - Tags with special characters
# - Tags with numbers
# - Multiple tags translation (if applicable)
# - Performance for large dictionaries (if relevant)