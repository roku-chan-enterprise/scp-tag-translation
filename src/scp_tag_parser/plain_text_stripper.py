import re
from .error_handler import ErrorHandler
from .logger import Logger
from .models import ErrorType

class PlainTextStripper:
    """
    Wikidot構文を除去してプレーンテキストを生成するクラス
    """

    def __init__(self, error_handler: ErrorHandler, logger: Logger):
        """
        Args:
            error_handler: エラーハンドラ
            logger: ロガー
        """
        self.error_handler = error_handler
        self.logger = logger

    def __call__(self, text: str) -> str:
        """
        Wikidot構文を除去してプレーンテキストを生成

        Args:
            text: Wikidot構文を含むテキスト

        Returns:
            プレーンテキスト
        """
        if not text:
            return ""

        self.logger.debug(f"PlainTextStripper: 処理開始 - 元テキスト長: {len(text)}")
        
        # 処理前のテキスト長
        original_length = len(text)
        
        # 1. リンクを処理
        # [[[page-slug|name]]] -> name, [[[page-slug]]] -> page-slug
        text = re.sub(r'\[\[\[([^|]+)\|([^\]]+)]]]', r'\2', text)
        text = re.sub(r'\[\[\[([^\]]+)]]]', r'\1', text)
        
        # 2. 通常リンクを処理
        # [page-slug|name] -> name, [page-slug] -> page-slug
        text = re.sub(r'\[(?:[^\s\[\]]+\s+)?([^|]+)\|([^\]]+)\]', r'\2', text)
        text = re.sub(r'\[(?:[^\s\[\]]+\s+)?([^\]]+)\]', r'\1', text)
        
        # 3. 装飾を除去
        # //italic// -> italic
        text = re.sub(r'//(.+?)//', r'\1', text)
        # **bold** -> bold
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        # __underline__ -> underline
        text = re.sub(r'__(.+?)__', r'\1', text)
        # --strikethrough-- -> strikethrough
        text = re.sub(r'--(.+?)--', r'\1', text)
        # {{monospace}} -> monospace
        text = re.sub(r'{{(.+?)}}', r'\1', text)
        
        # 4. その他のWikidot構文を除去
        # [[div]] ... [[/div]] -> 内容のみ残す
        text = re.sub(r'\[\[div(?:[^\]]*)]](.*?)\[\[/div]]', r'\1', text, flags=re.DOTALL)
        # [[span]] ... [[/span]] -> 内容のみ残す
        text = re.sub(r'\[\[span(?:[^\]]*)]](.*?)\[\[/span]]', r'\1', text, flags=re.DOTALL)
        # [[code]] ... [[/code]] -> 内容のみ残す
        text = re.sub(r'\[\[code(?:[^\]]*)]](.*?)\[\[/code]]', r'\1', text, flags=re.DOTALL)
        
        # 5. 残りの[[...]]タグを除去
        text = re.sub(r'\[\[.*?]]', '', text)
        
        # 6. 連続する空白を1つに
        text = re.sub(r'\s+', ' ', text)
        
        # 7. 前後の空白を除去
        text = text.strip()
        
        # 処理後のテキスト長
        processed_length = len(text)
        reduction = original_length - processed_length
        
        self.logger.debug(f"PlainTextStripper: 処理完了 - 結果テキスト長: {processed_length} ({reduction} 文字削減)")
        
        return text