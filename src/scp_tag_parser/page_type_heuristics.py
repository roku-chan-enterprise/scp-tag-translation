import re
from typing import List, Dict
from .error_handler import ErrorHandler
from .logger import Logger
from .models import ErrorType

class PageTypeHeuristics:
    """
    説明文からページ種別を推測するクラス
    """

    def __init__(self, error_handler: ErrorHandler, logger: Logger):
        """
        Args:
            error_handler: エラーハンドラ
            logger: ロガー
        """
        self.error_handler = error_handler
        self.logger = logger
        
        # ページ種別を示すキーワード辞書
        self.page_type_keywords = {
            "scp": ["SCP報告書", "オブジェクト", "アイテム", "//scp//"],
            "tale": ["Tale", "物語", "コンテンツ", "//tale//"],
            "goi-format": ["GoI", "フォーマット", "//goi-format//"],
            "guide": ["ガイド", "解説", "//ガイド//"],
            "supplement": ["補足", "サプリメント", "//補足//"],
            # その他のページ種別
        }
        
        # 「〜の記事に付与」パターン
        self.page_type_patterns = [
            (r"(SCP報告書|SCPオブジェクト)の記事に付与", ["scp"]),
            (r"//scp//(?:タグ|ページ|記事)(?:が付与されて|に付与|にしか付与でき)(?:いる|ない)", ["scp"]),
            (r"//tale//(?:タグ|ページ|記事)(?:が付与されて|に付与|にしか付与でき)(?:いる|ない)", ["tale"]),
            (r"//goi-format//(?:タグ|ページ|記事)(?:が付与されて|に付与|にしか付与でき)(?:いる|ない)", ["goi-format"]),
            (r"//補足//(?:タグ|ページ|記事)(?:が付与されて|に付与|にしか付与でき)(?:いる|ない)", ["補足"]),
        ]

    def __call__(self, text: str) -> List[str]:
        """
        説明文からページ種別を推測

        Args:
            text: 解析するテキスト

        Returns:
            ページ種別のリスト
        """
        if not text:
            return []

        detected_types = set()
        
        # パターンによる検出
        for pattern, types in self.page_type_patterns:
            if re.search(pattern, text):
                for t in types:
                    detected_types.add(t)
                    self.logger.debug(f"PageTypeHeuristics: パターン検出 - パターン: {pattern}, 種別: {t}")
        
        # キーワード辞書による検出
        for page_type, keywords in self.page_type_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    detected_types.add(page_type)
                    self.logger.debug(f"PageTypeHeuristics: キーワード検出 - キーワード: {keyword}, 種別: {page_type}")
        
        result = list(detected_types)
        self.logger.debug(f"PageTypeHeuristics: 合計 {len(result)} 件のページ種別を検出: {result}")
        return result