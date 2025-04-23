import re
from typing import Dict, List, Any
from .error_handler import ErrorHandler
from .logger import Logger
from .models import ErrorType
from .wikidot_link_scanner import WikidotLinkScanner
from .tag_mention_miner import TagMentionMiner
from .page_type_heuristics import PageTypeHeuristics
from .footnote_stripper import FootnoteStripper
from .plain_text_stripper import PlainTextStripper

class DescAnalyzer:
    """
    説明文を解析してメタ情報を抽出するクラス
    """

    def __init__(self, error_handler: ErrorHandler, logger: Logger):
        """
        Args:
            error_handler: エラーハンドラ
            logger: ロガー
        """
        self.error_handler = error_handler
        self.logger = logger
        
        # サブコンポーネントの初期化
        self.link_scanner = WikidotLinkScanner(error_handler, logger)
        self.tag_mention_miner = TagMentionMiner(error_handler, logger)
        self.page_type_heuristics = PageTypeHeuristics(error_handler, logger)
        self.footnote_stripper = FootnoteStripper(error_handler, logger)
        self.plain_text_stripper = PlainTextStripper(error_handler, logger)

    def __call__(self, description_raw: str) -> Dict[str, Any]:
        """
        説明文を解析してメタ情報を抽出

        Args:
            description_raw: 生の説明文

        Returns:
            メタ情報と平文説明文を含む辞書
        """
        if not description_raw:
            self.logger.warning("DescAnalyzer: 空の説明文が渡されました")
            return {
                "meta": {
                    "related_pages": [],
                    "related_tags": [],
                    "target_page_types": [],
                    "footnotes": [],
                    "other_notes": []
                },
                "description_plain": ""
            }

        self.logger.debug(f"DescAnalyzer: 処理開始 - 説明文長: {len(description_raw)}")
        
        try:
            # 1. Wikidotリンクの抽出
            links = self.link_scanner(description_raw)
            
            # 2. 関連タグの抽出
            related_tags = self.tag_mention_miner(description_raw, links)
            
            # 3. 対象ページ種別の推測
            page_types = self.page_type_heuristics(description_raw)
            
            # 4. 脚注の抽出
            footnotes, desc_without_footnotes = self.footnote_stripper(description_raw)
            
            # 5. その他の注意点の抽出
            other_notes = self._extract_other_notes(description_raw)
            
            # 6. プレーンテキストの生成
            plain_text = self.plain_text_stripper(desc_without_footnotes)
            
            result = {
                "meta": {
                    "related_pages": links,
                    "related_tags": related_tags,
                    "target_page_types": page_types,
                    "footnotes": footnotes,
                    "other_notes": other_notes
                },
                "description_plain": plain_text
            }
            
            self.logger.debug(f"DescAnalyzer: 処理完了 - 関連ページ: {len(links)}, 関連タグ: {len(related_tags)}, " +
                             f"ページ種別: {len(page_types)}, 脚注: {len(footnotes)}, その他注意点: {len(other_notes)}")
            
            return result
            
        except Exception as e:
            self.error_handler.handle_error(
                ErrorType.PARSE_ERROR,
                f"説明文の解析中にエラーが発生: {str(e)}",
                details={"exception": str(e), "description_raw": description_raw[:100] + "..."}
            )
            # エラー時は空の結果を返す
            return {
                "meta": {
                    "related_pages": [],
                    "related_tags": [],
                    "target_page_types": [],
                    "footnotes": [],
                    "other_notes": []
                },
                "description_plain": description_raw  # エラー時は元のテキストをそのまま返す
            }

    def _extract_other_notes(self, text: str) -> List[str]:
        """
        テキストからその他の注意点を抽出

        Args:
            text: 解析するテキスト

        Returns:
            注意点のリスト
        """
        notes = []
        
        # 必須条件の抽出
        for match in re.finditer(r"必ず.*(?:ください|必要があります|ねばなりません)", text):
            note = match.group(0).strip()
            notes.append(note)
            self.logger.debug(f"DescAnalyzer: 必須条件検出 - {note}")
        
        # 禁止事項の抽出
        for match in re.finditer(r"(?:使用|付与|併用)(?:でき)?(?:ない|ません)", text):
            # 前後のコンテキストを含める
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            context = text[start:end].strip()
            notes.append(context)
            self.logger.debug(f"DescAnalyzer: 禁止事項検出 - {context}")
        
        return notes