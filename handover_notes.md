## 引き継ぎ資料: SCPタグ翻訳プロジェクト テストケース修正タスク

**プロジェクト概要:**

*   **目的:** SCP財団日本支部(SCP-JP)のWikidotタグリストを解析し、英語タグと日本語タグの対応辞書を作成。その辞書を利用して、Webベースのタグ翻訳ツール (`index.html`) を提供する。
*   **主要成果物:**
    *   `dictionaries/en_to_jp.json`: 英語タグをキー、日本語タグを値とする翻訳辞書。
    *   `index.html`: 上記辞書を使用するタグ翻訳ツール。
    *   `src/`: タグリスト解析、辞書生成用のPythonスクリプト群。
    *   `data/`: 生データおよび処理済みタグデータ。
    *   `tests/`: テストスクリプト。

**現在の状況:**

1.  **データ生成:** Wikidotからのデータ取得、EN/JPタグリストの解析、`en_to_jp.json` 辞書の生成は完了済み。
2.  **翻訳ツール:** `index.html` は機能している。
3.  **テスト (`tests/test_translation.py`):**
    *   ユーザーの要望により、「現状の成果物（生成された辞書と翻訳関数の挙動）に合わせてテストケースを修正する」作業を実施中。
    *   `translate_tag` 関数は、辞書にキーが存在しない、または値が `null` の場合に `None` を返すように修正済み。
    *   `test_unknown_tag`, `test_empty_tag`, `test_case_sensitivity` の期待値を `None` に修正済み。
    *   `test_translation_of_specific_tags` 内の `test_cases` ディクショナリを一時的に空 `{}` にした状態。
    *   この状態で `pytest tests/test_translation.py` を実行すると、7件パス、1件スキップとなる。
4.  **課題:** `test_cases` ディクショナリを `dictionaries/en_to_jp.json` の内容に基づいて再生成し、`tests/test_translation.py` に反映させる段階で、`apply_diff` ツールの実行が複数回失敗している（diffフォーマットエラー、類似度不足エラー）。`write_to_file` もコンテンツ切り捨てエラーで失敗した経緯あり。ツールの挙動が不安定な可能性がある。

**直前の試行:**

*   `apply_diff` を使用して、空の `test_cases = {}` を、`dictionaries/en_to_jp.json` から生成した新しいディクショナリ文字列で置き換えようとしたが、diffフォーマットエラーで失敗した。

---

## 次のRooへのタスク指示 (Prompts)

<task>
**現在の状況:**
`tests/test_translation.py` 内の `test_translation_of_specific_tags` 関数のテストケース (`test_cases` ディクショナリ) が空になっています。このテストケースを、現在の `dictionaries/en_to_jp.json` ファイルの内容に基づいて再生成し、テストが全てパスするように修正してください。

**実行手順:**

1.  `dictionaries/en_to_jp.json` ファイルの内容を読み込みます。
2.  読み込んだJSONデータをパースし、値が `null` でないキーと値のペアのみを抽出します。
3.  抽出したデータを用いて、`test_translation_of_specific_tags` 関数内で使用する `test_cases` ディクショナリのPythonコード文字列を生成します（キーと値を適切に引用符で囲み、インデントを維持してください）。
4.  `tests/test_translation.py` の最新の内容を読み込みます。
5.  `apply_diff` ツールを使用して、`tests/test_translation.py` 内の空の `test_cases = {}` ブロック（前回の `read_file` 結果では94-95行目）を、手順3で生成した新しい `test_cases` ディクショナリの文字列で置き換えます。**注意:** `apply_diff` は過去に失敗しているため、`SEARCH` ブロックの内容と開始行を最新のファイル内容に合わせて慎重に指定してください。diffフォーマット (`<<<<<<< SEARCH`, `:start_line:`, `-------`, `=======`, `>>>>>>> REPLACE`) を厳守してください。
6.  `apply_diff` が成功したら、`pytest tests/test_translation.py` を実行し、全てのテスト（8件）がパスすることを確認します。
7.  全てのテストがパスしたら、`attempt_completion` ツールを使用して、テストケースの修正が完了したことを報告してください。

**代替案:**
もし `apply_diff` が再度失敗する場合は、`write_to_file` ツールを使用してファイル全体を書き換える方法を検討してください。その際は、ファイルの**完全な内容**を提供し、`test_cases` ディクショナリ部分のみを修正するようにしてください。
</task>