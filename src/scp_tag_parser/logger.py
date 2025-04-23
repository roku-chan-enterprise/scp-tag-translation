import logging
from enum import Enum
from .models import LogLevel

class Logger:
    """
    ロギング機能を提供するクラス
    """

    def __init__(self, log_level: LogLevel = LogLevel.INFO, log_file: str = None):
        """
        Args:
            log_level: ログレベル
            log_file: ログファイルのパス（Noneの場合はコンソールのみ）
        """
        self.logger = logging.getLogger("scp_tag_parser")
        self.logger.setLevel(getattr(logging, log_level.value)) # Use log_level.value

        # 既存のハンドラをクリア
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # フォーマッタの設定
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # コンソールハンドラの設定
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # ファイルハンドラの設定（指定されている場合）
        if log_file:
            try:
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            except Exception as e:
                self.logger.error(f"ログファイルハンドラの設定に失敗しました: {log_file} - {e}")

    def debug(self, message: str):
        """デバッグメッセージを出力"""
        self.logger.debug(message)

    def info(self, message: str):
        """情報メッセージを出力"""
        self.logger.info(message)

    def warning(self, message: str):
        """警告メッセージを出力"""
        self.logger.warning(message)

    def error(self, message: str):
        """エラーメッセージを出力"""
        self.logger.error(message)

    def critical(self, message: str):
        """致命的エラーメッセージを出力"""
        self.logger.critical(message)