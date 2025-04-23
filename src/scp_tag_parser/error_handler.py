from typing import Optional, Dict, List
from .models import ErrorType, ParserError
from .logger import Logger

class ErrorHandler:
    """
    エラーハンドリングを一元管理するクラス
    """

    def __init__(self, logger: Logger):
        """
        Args:
            logger: ロガーインスタンス
        """
        self.logger = logger
        self.errors: List[ParserError] = []

    def handle_error(self, error_type: ErrorType, message: str, source_file: str = None,
                    line_number: int = None, details: Dict = None, raise_exception: bool = False):
        """
        エラーを処理する

        Args:
            error_type: エラーの種類
            message: エラーメッセージ
            source_file: エラーが発生したソースファイル
            line_number: エラーが発生した行番号
            details: エラーの詳細情報
            raise_exception: 例外を発生させるかどうか

        Returns:
            処理されたエラー情報
        """
        error = ParserError(
            error_type=error_type,
            message=message,
            source_file=source_file,
            line_number=line_number,
            details=details
        )

        self.errors.append(error)

        # エラーレベルに応じてログ出力
        if error_type in [ErrorType.FILE_NOT_FOUND, ErrorType.CIRCULAR_REFERENCE]:
            self.logger.warning(f"{error_type.value}: {message}") # Use error_type.value
        else:
            self.logger.error(f"{error_type.value}: {message}") # Use error_type.value

        # 詳細情報があればログ出力
        if details:
            self.logger.debug(f"Details: {details}")

        # 例外を発生させる場合
        if raise_exception:
            raise Exception(f"{error_type.value}: {message}") # Use error_type.value

        return error

    def get_errors(self) -> List[ParserError]:
        """
        発生したエラーのリストを取得

        Returns:
            エラーのリスト
        """
        return self.errors

    def has_critical_errors(self) -> bool:
        """
        致命的なエラーが発生したかどうかを判定

        Returns:
            致命的なエラーが発生した場合はTrue
        """
        critical_types = [ErrorType.FILE_NOT_FOUND, ErrorType.PARSE_ERROR, ErrorType.VALIDATION_ERROR]
        return any(error.error_type in critical_types for error in self.errors)