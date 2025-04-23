from .error_handler import ErrorHandler
from .logger import Logger
from .models import ErrorType

class BasicFieldParser:
    """
    タグの基本フィールドを解析するクラス
    """

    def __init__(self, error_handler: ErrorHandler, logger: Logger):
        """
        Args:
            error_handler: エラーハンドラ
            logger: ロガー
        """
        self.error_handler = error_handler
        self.logger = logger

    def __call__(self, token: dict) -> dict:
        """
        タグ定義トークンから基本フィールドを抽出

        Args:
            token: タグ定義トークン (Lexerからの出力)

        Returns:
            基本フィールド情報
        """
        if token["type"] != "tag_definition":
            self.error_handler.handle_error(
                ErrorType.PARSE_ERROR,
                "タグ定義トークンではありません",
                line_number=token.get("line_number"),
                details={"token_type": token.get("type")}
            )
            # Return empty dict on error
            return {
                "slug": "",
                "name_jp": "",
                "name_en": None,
                "description_raw": ""
            }

        # 必須フィールドの検証
        slug = token.get("slug", "").strip()
        name_jp = token.get("name_jp", "").strip()
        description = token.get("description", "").strip()
        line_num = token.get("line_number")

        # スラッグのバリデーション
        if not slug:
            self.error_handler.handle_error(
                ErrorType.VALIDATION_ERROR,
                "タグスラッグが空です",
                line_number=line_num,
                details={"token": token}
            )

        # 日本語名のバリデーション
        if not name_jp:
            self.error_handler.handle_error(
                ErrorType.VALIDATION_ERROR,
                "タグの日本語名が空です",
                line_number=line_num,
                details={"token": token}
            )

        # 英語名の処理（オプショナル）
        name_en = token.get("name_en")
        if name_en:
            name_en = name_en.strip()
            if not name_en:  # 空文字列の場合はNoneに
                name_en = None

        # 説明文のバリデーション
        if not description:
            self.logger.warning(f"BasicFieldParser: 説明文が空です (L{line_num}) - スラッグ: {slug}")

        self.logger.debug(f"BasicFieldParser: 基本フィールド抽出 (L{line_num}) - スラッグ: {slug}, 日本語名: {name_jp}, 英語名: {name_en}")

        return {
            "slug": slug,
            "name_jp": name_jp,
            "name_en": name_en,
            "description_raw": description
        }