# SCP Tag Translation Tool

SCP財団のタグを多言語翻訳するための静的ツールです。
既存のタグをスペース区切り・連結タグの両方で入力し、一括して翻訳結果を得られます。

## 特長

- 英語(en)・日本語(jp)など複数の SCP 支部タグに対応（現在は en → jp のみ実装中）
- 連結タグ (例: `fireinscription`) を最長一致で分割して翻訳
- 未定義タグや非使用タグはログ表示
- ダークモード対応
- レスポンシブデザインにより、PC/モバイルどちらでも快適
- SCP Wiki 独自の「支部タグ」を翻訳結果に付加（例: 翻訳元が en なら訳結果に `en` タグを自動追加）

## デモ

[GitHub Pagesへのリンク](https://scp-jp.github.io/scp-tag-translation/index.html)

## 使い方

1. リポジトリをクローン or ダウンロード
2. `index.html` と `data/dictionaries/` ディレクトリを同階層に配置
3. ブラウザで `index.html` を開く
4. 翻訳元・翻訳先言語を選択 (現在は en→jp のみ選択可能)
5. 翻訳したいタグを入力すると、自動で翻訳結果が表示されます
6. 「コピー」ボタンで出力をクリップボードにコピー可能

## 辞書ファイル

- `data/dictionaries/en_to_jp.json` のように言語ペアごとにファイルを用意します
- 非使用タグは値に `null` を設定し、ログ表示のみ行います
- 未定義タグは辞書に含まれないため、ログで "(未定義)" と表示

## タグリスト解析システム

このリポジトリには、タグ翻訳ツールの辞書ファイルを生成するためのタグリスト解析システムも含まれています。このシステムは、SCP財団のWikidotソースからタグ情報を抽出し、構造化されたJSONファイルとして出力します。

### 機能

- タグ名（日本語）
- タグスラッグ（URL に使われる識別子）
- 英語タグ名（存在する場合）
- 説明文（Wikidot 構文を含む生データと、構文を除去したプレーンテキスト）
- カテゴリ階層
- 制限タグ情報（アイコンとその意味）
- メタ情報（説明文中の Wikidot リンク、関連タグ、対象ページ種別、注釈など）

### 使用方法

```bash
# パッケージをインストール
pip install -e .

# 基本的な使用方法
scp-tag-parser

# 入力ファイルと出力ファイルを指定
scp-tag-parser --input path/to/tag-list.txt --output path/to/output.json

# ヘルプを表示
scp-tag-parser --help
```

### セットアップと辞書データ生成の手順

タグ翻訳ツールを使用するためには、まず辞書データを生成する必要があります。以下に、リポジトリのセットアップから辞書データの生成、タグ翻訳ツールの使用までの一連の流れを説明します。

#### 1. リポジトリのセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/scp-jp/scp-tag-translation.git
cd scp-tag-translation

# 依存関係のインストール
pip install -e .
```

#### 2. 辞書データの生成

辞書データを生成するには、以下のいずれかの方法を使用できます：

**方法1: 一括処理（推奨）**

すべての処理を一度に実行するには、以下のコマンドを実行します：

```bash
python make_dict_and_test.py
```

このスクリプトは以下の処理を順番に実行します：

1. Wikidotページの取得 (`retrieve_wikidot_page.py`)
2. 英語タグの解析 (`parse_en_tags.py`)
3. 日本語タグの解析 (`scp_tag_parser`)
4. 翻訳辞書の生成 (`create_en_to_jp_dict.py`)
5. テスト実行

**方法2: 個別処理**

各ステップを個別に実行することもできます：

```bash
# 1. Wikidotページの取得
python src/retrieve_wikidot_page.py

# 2. 英語タグの解析
python src/parse_en_tags.py

# 3. 日本語タグの解析
scp-tag-parser

# 4. 翻訳辞書の生成
python src/create_en_to_jp_dict.py

# 5. テスト実行
pytest
```

#### 3. 生成された辞書データの確認

辞書データは以下の場所に生成されます：

- 英語タグデータ: `data/processed/en_tags.json`
- 日本語タグデータ: `data/processed/jp_tags_new.json`
- 翻訳辞書: `dictionaries/en_to_jp.json`

#### 4. タグ翻訳ツールの使用

辞書データが生成されたら、タグ翻訳ツールを使用できます：

1. ブラウザで `index.html` を開く
2. 翻訳元・翻訳先言語を選択 (現在は en→jp のみ選択可能)
3. 翻訳したいタグを入力すると、自動で翻訳結果が表示されます
4. 「コピー」ボタンで出力をクリップボードにコピー可能

### 処理フローの詳細

各ステップの詳細は以下の通りです：

1. **Wikidotページの取得** (`retrieve_wikidot_page.py`)
   - 英語版と日本語版のタグリストページをWikidotから取得
   - 取得したデータを `data/raw/wikidot_sources/` に保存

2. **英語タグの解析** (`parse_en_tags.py`)
   - 英語版タグリストを解析
   - 結果を `data/processed/en_tags.json` に保存

3. **日本語タグの解析** (`scp_tag_parser`)
   - 日本語版タグリストを解析
   - 結果を `data/processed/jp_tags_new.json` に保存

4. **翻訳辞書の生成** (`create_en_to_jp_dict.py`)
   - 英語タグと日本語タグのマッピングを作成
   - 結果を `dictionaries/en_to_jp.json` に保存

5. **テスト実行**
   - 生成された辞書データが正しく機能するかテスト

## 今後の拡張

- 他ペア対応： `xx_to_yy.json` を追加し、`index.html` の選択肢を有効化
- 多言語 UI への発展
- タグリスト解析システムの機能拡張（より詳細なメタ情報の抽出など）

## コントリビュート / ライセンス

- Pull Request 大歓迎です。新タグ・新ペアを追加する際は、対応する JSON ファイルを `data/dictionaries/` に置いてください
- 本ツールのソースコードは MIT ライセンスに準じます
