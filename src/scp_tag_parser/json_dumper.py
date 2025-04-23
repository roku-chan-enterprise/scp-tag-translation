import os
import json
import traceback
from typing import List, Any
from .error_handler import ErrorHandler
from .logger import Logger
from .models import ErrorType, Tag, Restriction

class JSONDumper:
    """
    タグデータをJSONファイルとして出力するクラス
    """

    def __init__(self, error_handler: ErrorHandler, logger: Logger):
        """
        Args:
            error_handler: エラーハンドラ
            logger: ロガー
        """
        self.error_handler = error_handler
        self.logger = logger

    def __call__(self, tags: List[Tag], output_path: str) -> bool:
        """
        タグデータをJSONファイルとして出力

        Args:
            tags: タグデータのリスト
            output_path: 出力ファイルパス

        Returns:
            成功した場合はTrue
        """
        self.logger.info(f"JSONDumper: JSON出力開始 - タグ数: {len(tags)}, 出力先: {output_path}")
        
        try:
            # 出力ディレクトリが存在しない場合は作成
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
                self.logger.debug(f"JSONDumper: 出力ディレクトリを作成 - {output_dir}")
            
            # JSONシリアライズ
            json_data = json.dumps(
                [tag.dict() for tag in tags],
                ensure_ascii=False,
                indent=2,
                default=self._json_serializer
            )
            
            # ファイル出力
            with open(output_path, 'w', encoding='utf-8', errors='replace') as f:
                f.write(json_data)
            
            self.logger.info(f"JSONDumper: JSON出力完了 - サイズ: {len(json_data)} バイト")
            return True
            
        except Exception as e:
            self.error_handler.handle_error(
                ErrorType.SERIALIZATION_ERROR,
                f"JSON出力中にエラーが発生: {str(e)}",
                details={
                    "output_path": output_path,
                    "exception": str(e),
                    "traceback": traceback.format_exc()
                }
            )
            return False

    def _json_serializer(self, obj: Any) -> Any:
        """
        JSONシリアライズできないオブジェクトを変換

        Args:
            obj: シリアライズ対象のオブジェクト

        Returns:
            シリアライズ可能な形式
        """
        # NamedTuple (Restriction) の処理
        if isinstance(obj, Restriction):
            return {
                "icon": obj.icon,
                "meaning": obj.meaning
            }
        
        # その他のオブジェクト
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        
        # 変換できない場合はエラー
        self.logger.error(f"JSONDumper: シリアライズできないオブジェクト - {type(obj)}")
        raise TypeError(f"Type {type(obj)} not serializable")