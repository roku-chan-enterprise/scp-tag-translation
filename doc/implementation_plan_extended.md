# SCP財団タグリスト解析システム実装計画（拡張版）

## 1. エラーハンドリングとロギング機能の追加

基本的な実装計画（`implementation_plan.md`）に加えて、以下のエラーハンドリングとロギング機能を追加します。

### 1.1 エラーハンドリング戦略

エラーハンドリングを一元管理するクラスを導入し、各コンポーネントで発生するエラーを統一的に処理します。

```python
from enum import Enum
from pydantic import BaseModel
from typing import Optional, Dict, List

# エラータイプの定義
class ErrorType(str, Enum):
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    CIRCULAR_REFERENCE = "CIRCULAR_REFERENCE"
    PARSE_ERROR = "PARSE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    SERIALIZATION_ERROR = "SERIALIZATION_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"

class ParserError(BaseModel):
    error_type: ErrorType
    message: str
    source_file: Optional[str] = None
    line_number: Optional[int] = None
    details: Optional[Dict] = None

class ErrorHandler:
    """
    エラーハンドリングを一元管理するクラス
    """
    
    def __init__(self, logger):
        """
        Args:
            logger: ロガーインスタンス
        """
        self.logger = logger
        self.errors: List[ParserError] = []
    
    def handle_error(self, error_type: ErrorType, message: str, source_file: str = None, 
                    line_number: int = None, details: Dict = None, raise_exception: bool = False):
        """
        エラーを処理する
        
        Args:
            error_type: エラーの種類
            message: エラーメッセージ
            source_file: エラーが発生したソースファイル
            line_number: エラーが発生した行番号
            details: エラーの詳細情報
            raise_exception: 例外を発生させるかどうか
            
        Returns:
            処理されたエラー情報
        """
        error = ParserError(
            error_type=error_type,
            message=message,
            source_file=source_file,
            line_number=line_number,
            details=details
        )
        
        self.errors.append(error)
        
        # エラーレベルに応じてログ出力
        if error_type in [ErrorType.FILE_NOT_FOUND, ErrorType.CIRCULAR_REFERENCE]:
            self.logger.warning(f"{error_type}: {message}")
        else:
            self.logger.error(f"{error_type}: {message}")
        
        # 詳細情報があればログ出力
        if details:
            self.logger.debug(f"Details: {details}")
        
        # 例外を発生させる場合
        if raise_exception:
            raise Exception(f"{error_type}: {message}")
        
        return error
    
    def get_errors(self) -> List[ParserError]:
        """
        発生したエラーのリストを取得
        
        Returns:
            エラーのリスト
        """
        return self.errors
    
    def has_critical_errors(self) -> bool:
        """
        致命的なエラーが発生したかどうかを判定
        
        Returns:
            致命的なエラーが発生した場合はTrue
        """
        critical_types = [ErrorType.FILE_NOT_FOUND, ErrorType.PARSE_ERROR, ErrorType.VALIDATION_ERROR]
        return any(error.error_type in critical_types for error in self.errors)
```

### 1.2 ロギング機能

ロギング機能を提供するクラスを導入し、各コンポーネントでのログ出力を統一的に管理します。

```python
import logging
from enum import Enum

# ログレベルの定義
class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class Logger:
    """
    ロギング機能を提供するクラス
    """
    
    def __init__(self, log_level: LogLevel = LogLevel.INFO, log_file: str = None):
        """
        Args:
            log_level: ログレベル
            log_file: ログファイルのパス（Noneの場合はコンソールのみ）
        """
        self.logger = logging.getLogger("scp_tag_parser")
        self.logger.setLevel(getattr(logging, log_level))
        
        # 既存のハンドラをクリア
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # フォーマッタの設定
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # コンソールハンドラの設定
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # ファイルハンドラの設定（指定されている場合）
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """デバッグメッセージを出力"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """情報メッセージを出力"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """警告メッセージを出力"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """エラーメッセージを出力"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """致命的エラーメッセージを出力"""
        self.logger.critical(message)
```

## 2. 各コンポーネントへのエラーハンドリングとロギングの統合

### 2.1 SourceLoader（エラーハンドリング対応版）

```python
class SourceLoader:
    """
    Wikidotソースファイルを読み込み、includeディレクティブを展開するクラス
    """
    
    def __init__(self, base_dir: str, error_handler: ErrorHandler, logger: Logger):
        """
        Args:
            base_dir: ファイルパスの基準ディレクトリ
            error_handler: エラーハンドラ
            logger: ロガー
        """
        self.base_dir = base_dir
        self.error_handler = error_handler
        self.logger = logger
        self.visited = set()  # 既に処理したファイル
        self.visiting = set()  # 処理中のファイル（循環検知用）
        
    def __call__(self, entry_file: str) -> str:
        """
        エントリーファイルを読み込み、includeを展開して完全なソースを返す
        
        Args:
            entry_file: 読み込むファイルのパス
            
        Returns:
            展開されたソーステキスト
        """
        self.logger.info(f"SourceLoader: 処理開始 - エントリーファイル: {entry_file}")
        result = self._process_file(entry_file)
        self.logger.info(f"SourceLoader: 処理完了 - 展開後のサイズ: {len(result)} バイト")
        return result
    
    def _process_file(self, file_path: str) -> str:
        """
        ファイルを読み込み、includeを再帰的に展開
        
        Args:
            file_path: 読み込むファイルのパス
            
        Returns:
            展開されたファイルの内容
        """
        full_path = os.path.normpath(os.path.join(self.base_dir, file_path))
        self.logger.debug(f"SourceLoader: ファイル処理 - {full_path}")
        
        # 循環参照チェック
        if full_path in self.visiting:
            self.error_handler.handle_error(
                ErrorType.CIRCULAR_REFERENCE,
                f"循環参照を検出: {file_path}",
                source_file=file_path
            )
            return f"<!-- Circular include: {file_path} -->"
        
        # 既に処理済みのファイルはスキップ（最適化）
        if full_path in self.visited:
            self.logger.debug(f"SourceLoader: 既に処理済みのファイル - {full_path}")
            return self._read_file(full_path)
        
        self.visiting.add(full_path)
        
        try:
            content = self._read_file(full_path)
            expanded_content = self._expand_includes(content, file_path)
            
            self.visited.add(full_path)
            self.visiting.remove(full_path)
            
            return expanded_content
            
        except FileNotFoundError:
            error = self.error_handler.handle_error(
                ErrorType.FILE_NOT_FOUND,
                f"ファイルが見つかりません: {file_path}",
                source_file=file_path
            )
            self.visiting.remove(full_path)
            return f"<!-- File not found: {file_path} -->"
        except Exception as e:
            error = self.error_handler.handle_error(
                ErrorType.UNKNOWN_ERROR,
                f"ファイル処理中にエラーが発生: {str(e)}",
                source_file=file_path,
                details={"exception": str(e)}
            )
            self.visiting.remove(full_path)
            return f"<!-- Error processing file: {file_path} - {str(e)} -->"
```

### 2.2 メインパイプライン（エラーハンドリング対応版）

```python
def parse_jp_tags_new(
    start_filepath: str = "tag-list.txt",
    output_filepath: str = os.path.join("data", "processed", "jp_tags_new.json"),
    base_dir: str = os.path.join("data", "raw", "wikidot_sources", "scp-jp"),
    log_level: LogLevel = LogLevel.INFO,
    log_file: str = None
) -> bool:
    """
    日本語版タグリストファイルを解析し、拡張されたタグ情報をJSON形式で出力する。
    
    Args:
        start_filepath: 開始ファイルのパス
        output_filepath: 出力JSONファイルのパス
        base_dir: ファイルパスの基準ディレクトリ
        log_level: ログレベル
        log_file: ログファイルのパス
        
    Returns:
        成功した場合はTrue
    """
    # ロガーとエラーハンドラの初期化
    logger = Logger(log_level, log_file)
    error_handler = ErrorHandler(logger)
    
    logger.info(f"タグリスト解析開始 - 入力: {os.path.join(base_dir, start_filepath)}, 出力: {output_filepath}")
    
    try:
        # 1. ソースローダー
        source_loader = SourceLoader(base_dir, error_handler, logger)
        source = source_loader(start_filepath)
        
        # 2. レキサー
        lexer = Lexer(source, error_handler, logger)
        tokens = lexer()
        
        # 3. エミッター
        emitter = Emitter(error_handler, logger)
        tags = emitter(tokens, start_filepath)
        
        # 4. JSONダンパー
        json_dumper = JSONDumper(error_handler, logger)
        result = json_dumper(tags, output_filepath)
        
        # 結果の出力
        errors = error_handler.get_errors()
        if errors:
            logger.warning(f"解析完了 - {len(errors)} 件のエラーが発生")
            for i, error in enumerate(errors[:10], 1):  # 最初の10件のみ表示
                logger.warning(f"エラー {i}: {error.error_type} - {error.message}")
            if len(errors) > 10:
                logger.warning(f"... 他 {len(errors) - 10} 件のエラー")
        
        logger.info(f"タグリスト解析完了 - {len(tags)} 件のタグを抽出")
        return result and not error_handler.has_critical_errors()
        
    except Exception as e:
        error_handler.handle_error(
            ErrorType.UNKNOWN_ERROR,
            f"予期しないエラーが発生: {str(e)}",
            details={"exception": str(e), "traceback": traceback.format_exc()}
        )
        logger.critical(f"タグリスト解析失敗 - {str(e)}")
        return False
```

## 3. テスト戦略（エラーハンドリング対応版）

### 3.1 ユニットテスト

各コンポーネントの機能を個別にテストします。エラーハンドリングとロギング機能のテストも含めます。

```python
def test_source_loader_with_error_handling():
    """SourceLoaderのエラーハンドリングテスト"""
    # テスト用の一時ファイルを作成
    with tempfile.TemporaryDirectory() as tmpdir:
        # ロガーとエラーハンドラの初期化
        logger = Logger(LogLevel.DEBUG)
        error_handler = ErrorHandler(logger)
        
        # 存在しないファイルのテスト
        loader = SourceLoader(tmpdir, error_handler, logger)
        result = loader("non_existent_file.txt")
        
        # エラーが記録されていることを確認
        errors = error_handler.get_errors()
        assert len(errors) == 1
        assert errors[0].error_type == ErrorType.FILE_NOT_FOUND
        
        # 循環参照のテスト
        circular_file = os.path.join(tmpdir, "fragment_circular.txt")
        with open(circular_file, 'w', encoding='utf-8') as f:
            f.write("[[include :scp-jp:fragment:circular]]\n")
        
        result = loader("fragment_circular.txt")
        
        # エラーが記録されていることを確認
        errors = error_handler.get_errors()
        assert len(errors) == 2  # 前のエラーと合わせて2つ
        assert errors[1].error_type == ErrorType.CIRCULAR_REFERENCE
```

### 3.2 結合テスト

パイプライン全体の機能をテストします。エラーケースも含めます。

```python
def test_full_pipeline_with_error_handling():
    """パイプライン全体のエラーハンドリングテスト"""
    # テスト用の一時ファイルを作成
    with tempfile.TemporaryDirectory() as tmpdir:
        # 正常なタグと不正なタグを含むテストファイル
        test_file = os.path.join(tmpdir, "test-tag-list.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("+ カテゴリ1[[# cat1]]\n")
            f.write("* **[[[/system:page-tags/tag/test-tag|テストタグ]]]** //(test-tag)// - これはテスト用のタグです。\n")
            f.write("* **[[[/system:page-tags/tag/|無効タグ]]]** - スラッグが空のタグ。\n")  # 不正なタグ
        
        # 出力ファイルパス
        output_file = os.path.join(tmpdir, "output.json")
        
        # パイプライン実行
        result = parse_jp_tags_new(
            start_filepath=os.path.basename(test_file),
            output_filepath=output_file,
            base_dir=tmpdir,
            log_level=LogLevel.DEBUG
        )
        
        # 結果の検証
        assert os.path.exists(output_file)
        
        # 出力JSONの検証
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert len(data) == 1  # 不正なタグは除外されている
            assert data[0]["slug"] == "test-tag"
```

## 4. 実装ロードマップ（拡張版）

1. **Day-1**: SourceLoader, Lexer, HeadingParser の実装
2. **Day-2**: TagDefDetector + RestrIconExtractor + BasicFieldParser の実装
3. **Day-3**: DescAnalyzer MVP (WikidotLinkScanner, FootnoteStripper, PlainTextStripper) の実装
4. **Day-4**: TagMentionMiner, PageTypeHeuristics の実装
5. **Day-5**: Emitter, DataNormalizer, JSONDumper の実装
6. **Day-6**: ErrorHandler, Logger の実装と各コンポーネントへの統合
7. **Day-7**: ユニットテスト + 結合テスト + 回帰テスト の実装
8. **Day-8**: ドキュメント + README + サンプル JSON の作成

## 5. 結論

この拡張版実装計画では、基本的な実装計画に加えて、エラーハンドリングとロギング機能を追加しました。これにより、以下の利点が得られます：

1. **堅牢性の向上**: 様々なエラーケースに対応し、システムの堅牢性が向上します。
2. **デバッグ容易性**: 詳細なログ出力により、問題の特定と解決が容易になります。
3. **保守性の向上**: エラーハンドリングとロギングを一元管理することで、コードの保守性が向上します。
4. **ユーザーエクスペリエンスの向上**: エラーメッセージの改善により、ユーザーが問題を理解しやすくなります。

これらの機能を追加することで、要件定義書で求められている「正確性」「網羅性」「柔軟性」「保守性」の要件をより高いレベルで満たすことができます。
