import re
from typing import List, Dict
from .error_handler import ErrorHandler
from .logger import Logger
from .models import ErrorType, RelatedTag, RelatedPage

class TagMentionMiner:
    """
    説明文から関連タグへの言及を抽出するクラス
    """

    def __init__(self, error_handler: ErrorHandler, logger: Logger):
        """
        Args:
            error_handler: エラーハンドラ
            logger: ロガー
        """
        self.error_handler = error_handler
        self.logger = logger
        
        # 関連タグを示す自然言語パターン
        self.patterns = [
            (r'//([^/]+)//タグと(?:は)?併用(?:でき)?(?:ない|ません)', '併用不可'),
            (r'//([^/]+)//タグ(?:を|の)(?:代わりに|代替として)(?:使用|使って)(?:して)?ください', '代替推奨'),
            (r'//([^/]+)//タグ(?:を|も)(?:参照|確認)(?:して)?ください', '参照推奨'),
            (r'必ず//([^/]+)//タグと併用(?:して)?(?:ください|する必要があります|されねばなりません)', '併用必須'),
            (r'適切(?:な)?(?:ら)?(?:ば)?//([^/]+)//タグと併用(?:して)?ください', '併用推奨'),
        ]
        
        # タグへの直接リンクを抽出するパターン
        self.tag_link_pattern = re.compile(r'\[\[\[/system:page-tags/tag/([^|]+)\|([^\]]+)]]]')
        
        # タグ名→スラッグのマッピング（実際の実装では、既知のタグのマッピングを保持する）
        self.tag_name_to_slug: Dict[str, str] = {}

    def __call__(self, text: str, links: List[RelatedPage]) -> List[RelatedTag]:
        """
        説明文から関連タグへの言及を抽出

        Args:
            text: 解析するテキスト
            links: 既に抽出されたリンク情報

        Returns:
            関連タグ情報のリスト
        """
        if not text:
            return []

        related_tags = []
        
        # 1. リンクからの抽出（/system:page-tags/tag/スラッグ形式）
        for match in self.tag_link_pattern.finditer(text):
            slug = match.group(1).strip()
            tag_name = match.group(2).strip()
            
            # タグ名→スラッグのマッピングを更新
            self.tag_name_to_slug[tag_name] = slug
            
            self.logger.debug(f"TagMentionMiner: タグリンク検出 - スラッグ: {slug}, 名前: {tag_name}")
            related_tags.append(RelatedTag(slug=slug, relation_type="リンク参照"))
        
        # 2. 自然言語パターンからの抽出
        for pattern, relation_type in self.patterns:
            for match in re.finditer(pattern, text):
                tag_name = match.group(1).strip()
                
                # タグ名からスラッグを推測
                slug = self._guess_slug_from_name(tag_name)
                
                if slug:
                    self.logger.debug(f"TagMentionMiner: 自然言語パターン検出 - タグ名: {tag_name}, 関係: {relation_type}")
                    related_tags.append(RelatedTag(slug=slug, relation_type=relation_type))
        
        self.logger.debug(f"TagMentionMiner: 合計 {len(related_tags)} 件の関連タグを検出")
        return related_tags

    def _guess_slug_from_name(self, name: str) -> str:
        """
        タグ名からスラッグを推測

        Args:
            name: タグ名

        Returns:
            推測されたスラッグ
        """
        # 1. 既知のマッピングを確認
        if name in self.tag_name_to_slug:
            return self.tag_name_to_slug[name]
        
        # 2. 簡易的な推測（実際の実装では、より高度な方法が必要）
        # 英数字のみの場合はそのまま、日本語の場合は英語に変換するなどの処理が必要
        # ここでは簡易的に小文字化して返す
        slug = name.lower()
        
        self.logger.debug(f"TagMentionMiner: スラッグ推測 - タグ名: {name} → スラッグ: {slug}")
        return slug