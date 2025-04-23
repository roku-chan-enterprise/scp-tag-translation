import re
from .error_handler import ErrorHandler
from .logger import Logger
from .models import ErrorType

class Lexer:
    """
    ソーステキストを行単位でトークン化するクラス
    """

    def __init__(self, source: str, error_handler: ErrorHandler, logger: Logger):
        """
        Args:
            source: 解析するソーステキスト
            error_handler: エラーハンドラ
            logger: ロガー
        """
        self.lines = source.splitlines()
        self.current_line_index = 0 # Renamed from current_line for clarity
        self.total_lines = len(self.lines)
        self.error_handler = error_handler
        self.logger = logger

        # 正規表現パターン (クラス変数として定義)
        self.heading_pattern = re.compile(r"^(?P<lvl>\+{1,2})\s*(?P<title>[^\[]+?)(?:\s*\[\[#\s*(?P<id>[^\]]+)]])?")
        # Tag pattern needs careful review based on fragment_tag-list-basic.txt examples
        # Original plan pattern: r'^[ \t\u3000]*\*[ \t\u3000]*(?:,,[^,]+,,[ \t\u3000]*)*\*\*\[\[\[/system:page-tags/tag/(?P<slug>[^|]+)\|(?P<jp>[^]]+)]]](?:\*\*)?[ \t\u3000]*(?://\((?P<en>[^)]+)\)//[ \t\u3000]*)?-\s*(?P<desc>.*)'
        # Let's refine it slightly for robustness, allowing optional bolding and optional EN part
        self.tag_pattern = re.compile(
            r"^[ \t\u3000]*\*[ \t\u3000]*"                                      # Leading asterisk and spaces
            r"(?P<icons>(?:,,[^,]+,,[ \t\u3000]*)*)"                           # Optional restriction icons
            r"(?:\*\*)?"                                                       # Optional starting bold
            r"\[\[\[/system:page-tags/tag/(?P<slug>[^|]+)\|(?P<jp>[^]]+)]]]"  # Tag link itself
            r"(?:\*\*)?"                                                       # Optional ending bold
            r"[ \t\u3000]*"                                                    # Optional spaces
            r"(?://\((?P<en>[^)]+)\)//[ \t\u3000]*)?"                         # Optional English name //(en)//
            r"-\s*"                                                            # Separator dash and spaces
            r"(?P<desc>.*)"                                                    # Description (rest of the line)
        )


    def __call__(self) -> list:
        """
        ソーステキストをトークン化

        Returns:
            トークンのリスト
        """
        self.logger.info(f"Lexer: トークン化開始 - 行数: {self.total_lines}")
        tokens = []

        while self.current_line_index < self.total_lines:
            try:
                token = self._next_token()
                if token:
                    tokens.append(token)
                    if token["type"] == "heading":
                        self.logger.debug(f"Lexer: 見出し検出 (L{token['line_number']}) - レベル: {token['level']}, タイトル: {token['title']}")
                    elif token["type"] == "tag_definition":
                        self.logger.debug(f"Lexer: タグ定義検出 (L{token['line_number']}) - スラッグ: {token['slug']}, 名前: {token['name_jp']}")
            except Exception as e:
                line_num = self.current_line_index + 1
                line = self.lines[self.current_line_index] if self.current_line_index < self.total_lines else ""
                self.error_handler.handle_error(
                    ErrorType.PARSE_ERROR,
                    f"行 {line_num} の解析中に予期せぬエラーが発生: {str(e)}",
                    line_number=line_num,
                    details={"line": line, "exception": str(e)}
                )
                # Move to the next line even if an error occurs in the current one
                self.current_line_index += 1

        self.logger.info(f"Lexer: トークン化完了 - トークン数: {len(tokens)}")
        return tokens

    def _next_token(self) -> dict | None: # Added None return type
        """
        次のトークンを取得

        Returns:
            トークン（辞書形式）または None
        """
        if self.current_line_index >= self.total_lines:
            return None

        line = self.lines[self.current_line_index]
        line_num = self.current_line_index + 1
        self.current_line_index += 1 # Increment index for the next call

        # 見出し行の処理
        heading_match = self.heading_pattern.match(line)
        if heading_match:
            return self._parse_heading(heading_match, line, line_num)

        # タグ定義行の処理
        tag_match = self.tag_pattern.match(line)
        if tag_match:
            return self._parse_tag_definition(tag_match, line, line_num)

        # その他の行は無視 (ログ出力もしない)
        # self.logger.debug(f"Lexer: 無視された行 (L{line_num}): {line[:80]}...") # Optional: Log ignored lines
        return None

    def _parse_heading(self, match: re.Match, line: str, line_num: int) -> dict:
        """
        見出し行を解析

        Args:
            match: 正規表現のマッチオブジェクト
            line: 解析する行
            line_num: 行番号

        Returns:
            見出しトークン
        """
        return {
            "type": "heading",
            "level": len(match.group("lvl")),
            "title": match.group("title").strip(),
            "id": match.group("id").strip() if match.group("id") else None,
            "line_number": line_num,
            "source_line": line
        }

    def _parse_tag_definition(self, match: re.Match, line: str, line_num: int) -> dict:
        """
        タグ定義行を解析 (複数行の説明文も考慮)

        Args:
            match: 正規表現のマッチオブジェクト
            line: 解析する行
            line_num: 行番号

        Returns:
            タグ定義トークン
        """
        # Extract initial description part
        description_lines = [match.group("desc").strip()]

        # Look ahead for continuation lines
        start_lookahead_index = self.current_line_index
        while self.current_line_index < self.total_lines:
            next_line = self.lines[self.current_line_index]
            # Check if the next line is a heading or another tag definition
            if self.heading_pattern.match(next_line) or self.tag_pattern.match(next_line):
                break
            # Check if it's likely a continuation (e.g., indented, not starting with '*')
            # This heuristic might need refinement based on actual data patterns
            if next_line.strip() and not next_line.strip().startswith("*") and not next_line.strip().startswith("+"):
                 # Consider lines starting with spaces/tabs as continuation
                 if next_line.startswith((' ', '\t', '\u3000')):
                     description_lines.append(next_line.strip())
                     self.current_line_index += 1
                 else:
                     # If it doesn't look like a continuation, stop.
                     break
            else:
                 # Stop if it's an empty line or looks like another definition/heading
                 break


        full_description = "\n".join(description_lines).strip()

        return {
            "type": "tag_definition",
            "icons": match.group("icons").strip(),
            "slug": match.group("slug").strip(),
            "name_jp": match.group("jp").strip(),
            "name_en": match.group("en").strip() if match.group("en") else None,
            "description": full_description,
            "line_number": line_num,
            "source_line": line # Store the original first line for reference
        }

    # _parse_tag_definition_tolerant is removed as the main pattern is made more robust