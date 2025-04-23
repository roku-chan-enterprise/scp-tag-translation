from .error_handler import ErrorHandler
from .logger import Logger
from .models import ErrorType

class HeadingParser:
    """
    見出しトークンからカテゴリ階層を構築するクラス
    """

    def __init__(self, error_handler: ErrorHandler, logger: Logger):
        """
        Args:
            error_handler: エラーハンドラ
            logger: ロガー
        """
        self.current_path: list[str] = []  # カテゴリパスのスタック
        self.error_handler = error_handler
        self.logger = logger

    def __call__(self, token: dict) -> list[str]:
        """
        トークンを処理し、現在のカテゴリパスを返す

        Args:
            token: 処理するトークン (Lexerからの出力)

        Returns:
            現在のカテゴリパス (例: ["基本的なタグ", "創作物"])
        """
        if token["type"] != "heading":
            # 見出しトークン以外が渡された場合は、現在のパスをそのまま返す
            return self.current_path.copy()

        level = token.get("level")
        title = token.get("title")
        line_num = token.get("line_number")

        if level is None or title is None:
            self.error_handler.handle_error(
                ErrorType.PARSE_ERROR,
                f"無効な見出しトークンです: レベルまたはタイトルがありません",
                line_number=line_num,
                details={"token": token}
            )
            return self.current_path.copy() # Return current path on error

        self.logger.debug(f"HeadingParser: 処理中 (L{line_num}) - レベル: {level}, タイトル: {title}")

        # レベルに応じてパスを更新
        if level == 1:
            self.current_path = [title]
            self.logger.debug(f"HeadingParser: パス更新 (レベル1) - {self.current_path}")
        elif level == 2:
            if not self.current_path:
                # レベル1の見出しがない状態でレベル2が見つかった場合
                self.logger.warning(f"HeadingParser: レベル1の見出しがない状態でレベル2が見つかりました (L{line_num}) - タイトル: {title}")
                self.current_path = ["不明な親カテゴリ", title] # 仮の親カテゴリを設定
            elif len(self.current_path) == 1:
                # 正常なレベル2
                self.current_path.append(title)
                self.logger.debug(f"HeadingParser: パス更新 (レベル2) - {self.current_path}")
            else: # len(self.current_path) >= 2
                # 既にレベル2が存在する場合、最後の要素を置き換える
                self.logger.debug(f"HeadingParser: パス置き換え (レベル2) - {self.current_path[-1]} -> {title}")
                self.current_path[-1] = title
        else:
            # 想定外のレベル
             self.error_handler.handle_error(
                ErrorType.PARSE_ERROR,
                f"想定外の見出しレベルです: {level}",
                line_number=line_num,
                details={"token": token}
            )

        return self.current_path.copy()

    def get_current_path(self) -> list[str]:
        """現在のカテゴリパスを取得する"""
        return self.current_path.copy()