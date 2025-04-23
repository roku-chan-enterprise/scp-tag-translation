import re
from typing import List
from .error_handler import ErrorHandler
from .logger import Logger
from .models import ErrorType, Restriction

class RestrIconExtractor:
    """
    制限アイコンとその意味を抽出するクラス
    """

    def __init__(self, error_handler: ErrorHandler, logger: Logger):
        """
        Args:
            error_handler: エラーハンドラ
            logger: ロガー
        """
        self.error_handler = error_handler
        self.logger = logger
        
        # アイコンと意味のマッピング
        # fragment_tag-list-basic.txtの冒頭に定義されている
        self.icon_meanings = {
            "︁": "使用禁止",      # ,,︁,,
            "": "編集禁止",       # ,,,,
            "": "制限緩和/翻訳",  # ,,,,
            "": "星マーク",       # ,,,, (他の星マーク付きタグと併用不可)
            # その他のアイコンマッピングは必要に応じて追加
        }
        
        # アイコン抽出用の正規表現
        self.icon_pattern = re.compile(r',,[^,]+,,')

    def __call__(self, icons_str: str) -> List[Restriction]:
        """
        アイコン文字列から制限情報のリストを抽出

        Args:
            icons_str: アイコンを含む文字列 (例: ",,︁,,,,,,")

        Returns:
            制限情報のリスト
        """
        if not icons_str or icons_str.strip() == "":
            return []

        self.logger.debug(f"RestrIconExtractor: アイコン文字列の処理 - {repr(icons_str)}")
        restrictions = []

        # カンマで区切られたアイコンを抽出
        for match in self.icon_pattern.finditer(icons_str):
            icon_with_commas = match.group(0)  # ,,アイコン,,
            icon = icon_with_commas.strip(',') # アイコン部分のみ抽出
            
            if icon in self.icon_meanings:
                meaning = self.icon_meanings[icon]
                self.logger.debug(f"RestrIconExtractor: アイコン検出 - {repr(icon)} ({meaning})")
                restrictions.append(Restriction(icon=icon, meaning=meaning))
            else:
                self.logger.warning(f"RestrIconExtractor: 未知のアイコン - {repr(icon)}")
                self.error_handler.handle_error(
                    ErrorType.PARSE_ERROR,
                    f"未知の制限アイコンです: {repr(icon)}",
                    details={"icon": icon, "icons_str": icons_str}
                )
                # 未知のアイコンも「不明なアイコン」として追加
                restrictions.append(Restriction(icon=icon, meaning="不明なアイコン"))

        return restrictions