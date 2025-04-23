import re
from typing import List, Tuple
from .error_handler import ErrorHandler
from .logger import Logger
from .models import ErrorType

class FootnoteStripper:
    """
    脚注を抽出し、本文から除去するクラス
    """

    def __init__(self, error_handler: ErrorHandler, logger: Logger):
        """
        Args:
            error_handler: エラーハンドラ
            logger: ロガー
        """
        self.error_handler = error_handler
        self.logger = logger
        
        # 脚注を抽出する正規表現
        # [[footnote]]脚注内容[[/footnote]] の形式
        self.footnote_pattern = re.compile(r'\[\[footnote]](.+?)(?:\[\[/footnote]]|$)', re.DOTALL)

    def __call__(self, text: str) -> Tuple[List[str], str]:
        """
        テキストから脚注を抽出し、本文から除去

        Args:
            text: 解析するテキスト

        Returns:
            (脚注のリスト, 脚注を除去したテキスト)
        """
        if not text:
            return [], ""

        footnotes = []
        
        def replace_footnote(match):
            footnote_text = match.group(1).strip()
            footnotes.append(footnote_text)
            self.logger.debug(f"FootnoteStripper: 脚注検出 - {footnote_text[:50]}...")
            return ""  # 脚注を空文字に置換
        
        # 脚注を抽出して除去
        text_without_footnotes = self.footnote_pattern.sub(replace_footnote, text)
        
        # 閉じタグがない脚注がある場合の警告
        if "[[footnote]]" in text_without_footnotes:
            self.logger.warning("FootnoteStripper: 閉じタグのない脚注が検出されました")
            self.error_handler.handle_error(
                ErrorType.PARSE_ERROR,
                "閉じタグのない脚注が検出されました",
                details={"text": text_without_footnotes}
            )
        
        self.logger.debug(f"FootnoteStripper: 合計 {len(footnotes)} 件の脚注を抽出")
        return footnotes, text_without_footnotes