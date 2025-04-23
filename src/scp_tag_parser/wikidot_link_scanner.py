import re
from typing import List
from .error_handler import ErrorHandler
from .logger import Logger
from .models import ErrorType, RelatedPage

class WikidotLinkScanner:
    """
    Wikidotリンクを抽出するクラス
    """

    def __init__(self, error_handler: ErrorHandler, logger: Logger):
        """
        Args:
            error_handler: エラーハンドラ
            logger: ロガー
        """
        self.error_handler = error_handler
        self.logger = logger
        
        # トリプルリンク [[[page-slug]]] や [[[page-slug|表示名]]] を抽出
        self.triple_link_pattern = re.compile(r'\[\[\[(?P<target>[^|\]]+)(?:\|(?P<disp>[^\]]+))?]]]')
        
        # 通常リンク [page-slug] や [page-slug|表示名] を抽出
        self.link_pattern = re.compile(r'\[(?:/|[^\s\[\]]+\s+)?(?P<target>[^\[\]|]+)(?:\|(?P<disp>[^\[\]]+))?\]')
        
        # タグへのリンクパターン
        self.tag_link_pattern = re.compile(r'/system:page-tags/tag/')

    def __call__(self, text: str) -> List[RelatedPage]:
        """
        テキストからWikidotリンクを抽出

        Args:
            text: 解析するテキスト

        Returns:
            リンク情報のリスト
        """
        if not text:
            return []

        links = []
        
        # トリプルリンクの抽出
        for match in self.triple_link_pattern.finditer(text):
            target = match.group("target").strip()
            display = match.group("disp").strip() if match.group("disp") else None
            
            # タグへのリンクは別途処理するため、ここでは通常のページリンクのみ扱う
            if not self.tag_link_pattern.search(target):
                self.logger.debug(f"WikidotLinkScanner: トリプルリンク検出 - ターゲット: {target}, 表示名: {display}")
                links.append(RelatedPage(slug=target, display_name=display))
        
        # 通常リンクの抽出
        for match in self.link_pattern.finditer(text):
            target = match.group("target").strip()
            display = match.group("disp").strip() if match.group("disp") else None
            
            # タグへのリンクは除外
            if not self.tag_link_pattern.search(target):
                self.logger.debug(f"WikidotLinkScanner: 通常リンク検出 - ターゲット: {target}, 表示名: {display}")
                links.append(RelatedPage(slug=target, display_name=display))
        
        self.logger.debug(f"WikidotLinkScanner: 合計 {len(links)} 件のリンクを検出")
        return links