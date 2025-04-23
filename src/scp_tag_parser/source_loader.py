import os
import re
from .error_handler import ErrorHandler
from .logger import Logger
from .models import ErrorType

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
        # include_pattern = re.compile(r"\[\[include\s+:scp-jp:(?:fragment:)?([^\]]+)\]\]") # Original pattern
        self.include_pattern = re.compile(r"\[\[include\s+:[^:\]]+:(?:fragment:)?([^\]\s]+)]]") # Pattern from plan

    def __call__(self, entry_file: str) -> str:
        """
        エントリーファイルを読み込み、includeを展開して完全なソースを返す

        Args:
            entry_file: 読み込むファイルのパス

        Returns:
            展開されたソーステキスト
        """
        self.logger.info(f"SourceLoader: 処理開始 - エントリーファイル: {entry_file}")
        # Reset visited and visiting sets for each top-level call
        self.visited = set()
        self.visiting = set()
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
        # Resolve the full path relative to the base directory
        # Handle cases where file_path might already be relative to base_dir
        if os.path.isabs(file_path):
             full_path = os.path.normpath(file_path)
        else:
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
        # Note: This optimization might be problematic if the same fragment is included multiple times
        # in different contexts. Consider removing if issues arise.
        # if full_path in self.visited:
        #     self.logger.debug(f"SourceLoader: 既に処理済みのファイル - {full_path}")
        #     # Re-reading might be safer than caching if content could differ based on context
        #     try:
        #         return self._read_file(full_path)
        #     except FileNotFoundError:
        #          # Handle case where cached file is no longer available (unlikely but possible)
        #          self.error_handler.handle_error(
        #              ErrorType.FILE_NOT_FOUND,
        #              f"キャッシュされたファイルが見つかりません: {file_path}",
        #              source_file=file_path
        #          )
        #          return f"<!-- Cached file not found: {file_path} -->"


        self.visiting.add(full_path)

        try:
            content = self._read_file(full_path)
            expanded_content = self._expand_includes(content, file_path)

            self.visited.add(full_path) # Mark as visited after successful processing
            self.visiting.remove(full_path)

            return expanded_content

        except FileNotFoundError:
            error = self.error_handler.handle_error(
                ErrorType.FILE_NOT_FOUND,
                f"ファイルが見つかりません: {file_path} (Full path: {full_path})",
                source_file=file_path
            )
            self.visiting.remove(full_path)
            return f"<!-- File not found: {file_path} -->"
        except Exception as e:
            error = self.error_handler.handle_error(
                ErrorType.UNKNOWN_ERROR,
                f"ファイル処理中にエラーが発生 ({file_path}): {str(e)}",
                source_file=file_path,
                details={"exception": str(e)}
            )
            # Ensure we remove from visiting even if an error occurs
            if full_path in self.visiting:
                self.visiting.remove(full_path)
            return f"<!-- Error processing file: {file_path} - {str(e)} -->"

    def _expand_includes(self, content: str, current_file: str) -> str:
        """
        includeディレクティブを展開

        Args:
            content: 展開するコンテンツ
            current_file: 現在処理中のファイル名

        Returns:
            展開されたコンテンツ
        """
        expanded_parts = []
        last_end = 0

        for match in self.include_pattern.finditer(content):
            start, end = match.span()
            fragment_name = match.group(1)
            self.logger.debug(f"SourceLoader: Include検出 - {fragment_name} in {current_file}")

            # Add content before the include directive
            expanded_parts.append(content[last_end:start])

            # Resolve and process the included fragment
            fragment_path = self._resolve_fragment_path(fragment_name)
            included_content = self._process_file(fragment_path)
            expanded_parts.append(included_content)

            last_end = end

        # Add remaining content after the last include directive
        expanded_parts.append(content[last_end:])

        return "".join(expanded_parts)


    def _resolve_fragment_path(self, fragment_name: str) -> str:
        """
        フラグメント名からファイルパスを解決 (base_dir基準)

        Args:
            fragment_name: フラグメント名 (例: test, tag-list-basic)

        Returns:
            解決されたファイルパス (例: fragment_test.txt)
        """
        # Wikidotの命名規則に合わせる
        if not fragment_name.startswith("fragment_"):
             filename = f"fragment_{fragment_name}"
        else:
             filename = fragment_name

        if not filename.endswith(".txt"):
             filename += ".txt"

        # Return the path relative to the base_dir, _process_file will join it
        # This assumes fragments are always in the same directory as the entry file or specified by base_dir
        return filename


    def _read_file(self, file_path: str) -> str:
        """
        ファイルを読み込む

        Args:
            file_path: 読み込むファイルのフルパス

        Returns:
            ファイルの内容
        """
        self.logger.debug(f"SourceLoader: ファイル読み込み - {file_path}")
        try:
            # 日本語Windowsでは、cp932（Shift-JIS）を優先的に試す
            encodings = ['cp932', 'utf-8', 'euc-jp', 'iso-2022-jp']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                        self.logger.debug(f"SourceLoader: ファイル読み込み成功 - エンコーディング: {encoding}")
                        return content
                except UnicodeDecodeError:
                    continue
            
            # 全てのエンコーディングが失敗した場合は、バイナリモードで読み込み、UTF-8に変換
            with open(file_path, 'rb') as f:
                binary_content = f.read()
                # バイナリデータをUTF-8として解釈（エラーは置換）
                content = binary_content.decode('utf-8', errors='replace')
                self.logger.warning(f"SourceLoader: エンコーディング検出失敗 - {file_path}, バイナリから変換")
                return content
        except FileNotFoundError:
            self.logger.error(f"SourceLoader: ファイル読み込みエラー - {file_path} が見つかりません")
            raise # Re-raise the exception to be caught by _process_file
        except Exception as e:
            self.logger.error(f"SourceLoader: ファイル読み込み中に予期せぬエラー - {file_path}: {e}")
            raise # Re-raise the exception