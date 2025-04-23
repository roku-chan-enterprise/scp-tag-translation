from typing import List, Dict, Any
from .error_handler import ErrorHandler
from .logger import Logger
from .models import ErrorType, Tag, Meta, SourceLocation
from .heading_parser import HeadingParser
from .restr_icon_extractor import RestrIconExtractor
from .basic_field_parser import BasicFieldParser
from .desc_analyzer import DescAnalyzer

class Emitter:
    """
    トークンからタグデータ構造を生成するクラス
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
        self.heading_parser = HeadingParser(error_handler, logger)
        self.restr_icon_extractor = RestrIconExtractor(error_handler, logger)
        self.basic_field_parser = BasicFieldParser(error_handler, logger)
        self.desc_analyzer = DescAnalyzer(error_handler, logger)

    def __call__(self, tokens: List[Dict[str, Any]], source_file: str) -> List[Tag]:
        """
        トークンリストからタグデータ構造を生成

        Args:
            tokens: トークンのリスト (Lexerからの出力)
            source_file: ソースファイル名

        Returns:
            タグデータのリスト
        """
        self.logger.info(f"Emitter: タグデータ生成開始 - トークン数: {len(tokens)}")
        tags = []
        current_category_path = []
        
        for token in tokens:
            try:
                if token["type"] == "heading":
                    # 見出しトークンの処理
                    current_category_path = self.heading_parser(token)
                    self.logger.debug(f"Emitter: カテゴリパス更新 - {current_category_path}")
                
                elif token["type"] == "tag_definition":
                    # タグ定義トークンの処理
                    self.logger.debug(f"Emitter: タグ定義処理 (L{token['line_number']}) - スラッグ: {token.get('slug')}")
                    
                    # 1. 基本フィールドの解析
                    tag_data = self.basic_field_parser(token)
                    
                    # 2. 制限アイコンの解析
                    restrictions = self.restr_icon_extractor(token.get("icons", ""))
                    
                    # 3. 説明文の詳細解析
                    desc_analysis = self.desc_analyzer(tag_data["description_raw"])
                    
                    # 4. タグデータの構築
                    try:
                        tag = Tag(
                            slug=tag_data["slug"],
                            name_jp=tag_data["name_jp"],
                            name_en=tag_data["name_en"],
                            description_raw=tag_data["description_raw"],
                            description_plain=desc_analysis["description_plain"],
                            category_path=current_category_path.copy() if current_category_path else ["未分類"],
                            restrictions=restrictions,
                            meta=Meta(
                                related_pages=desc_analysis["meta"]["related_pages"],
                                related_tags=desc_analysis["meta"]["related_tags"],
                                target_page_types=desc_analysis["meta"]["target_page_types"],
                                footnotes=desc_analysis["meta"]["footnotes"],
                                other_notes=desc_analysis["meta"]["other_notes"]
                            ),
                            source_location=SourceLocation(
                                file=source_file,
                                line=token["line_number"]
                            )
                        )
                        
                        tags.append(tag)
                        self.logger.debug(f"Emitter: タグ生成完了 - スラッグ: {tag.slug}, カテゴリ: {tag.category_path}")
                    
                    except Exception as e:
                        self.error_handler.handle_error(
                            ErrorType.VALIDATION_ERROR,
                            f"タグデータのバリデーションエラー: {str(e)}",
                            source_file=source_file,
                            line_number=token["line_number"],
                            details={"slug": tag_data["slug"], "exception": str(e)}
                        )
            
            except Exception as e:
                self.error_handler.handle_error(
                    ErrorType.PARSE_ERROR,
                    f"トークン処理中にエラーが発生: {str(e)}",
                    source_file=source_file,
                    line_number=token.get("line_number"),
                    details={"token_type": token.get("type"), "exception": str(e)}
                )
        
        self.logger.info(f"Emitter: タグデータ生成完了 - タグ数: {len(tags)}")
        return tags