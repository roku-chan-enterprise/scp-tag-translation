import os
import argparse
import traceback
from .models import LogLevel, ErrorType
from .logger import Logger
from .error_handler import ErrorHandler
from .source_loader import SourceLoader
from .lexer import Lexer
from .emitter import Emitter
from .json_dumper import JSONDumper

def parse_jp_tags(
    start_filepath: str = "tag-list.txt",
    output_filepath: str = os.path.join("data", "processed", "jp_tags_new.json"),
    base_dir: str = os.path.join("data", "raw", "wikidot_sources", "scp-jp"),
    log_level: LogLevel = LogLevel.INFO,
    log_file: str = None
) -> bool:
    """
    日本語版タグリストファイルを解析し、拡張されたタグ情報をJSON形式で出力する。

    Args:
        start_filepath: 開始ファイルのパス
        output_filepath: 出力JSONファイルのパス
        base_dir: ファイルパスの基準ディレクトリ
        log_level: ログレベル
        log_file: ログファイルのパス

    Returns:
        成功した場合はTrue
    """
    # ロガーとエラーハンドラの初期化
    logger = Logger(log_level, log_file)
    error_handler = ErrorHandler(logger)
    
    logger.info(f"タグリスト解析開始 - 入力: {os.path.join(base_dir, start_filepath)}, 出力: {output_filepath}")
    
    try:
        # 1. ソースローダー
        source_loader = SourceLoader(base_dir, error_handler, logger)
        source = source_loader(start_filepath)
        
        # 2. レキサー
        lexer = Lexer(source, error_handler, logger)
        tokens = lexer()
        
        # 3. エミッター
        emitter = Emitter(error_handler, logger)
        tags = emitter(tokens, start_filepath)
        
        # 4. JSONダンパー
        json_dumper = JSONDumper(error_handler, logger)
        result = json_dumper(tags, output_filepath)
        
        # 結果の出力
        errors = error_handler.get_errors()
        if errors:
            logger.warning(f"解析完了 - {len(errors)} 件のエラーが発生")
            for i, error in enumerate(errors[:10], 1):  # 最初の10件のみ表示
                logger.warning(f"エラー {i}: {error.error_type.value}: {error.message}")
            if len(errors) > 10:
                logger.warning(f"... 他 {len(errors) - 10} 件のエラー")
        
        logger.info(f"タグリスト解析完了 - {len(tags)} 件のタグを抽出")
        return result and not error_handler.has_critical_errors()
        
    except Exception as e:
        error_handler.handle_error(
            ErrorType.UNKNOWN_ERROR,
            f"予期しないエラーが発生: {str(e)}",
            details={"exception": str(e), "traceback": traceback.format_exc()}
        )
        logger.critical(f"タグリスト解析失敗 - {str(e)}")
        return False

def main():
    """コマンドラインからの実行をサポートするメイン関数"""
    parser = argparse.ArgumentParser(description='SCP財団日本語Wikiのタグリスト解析システム')
    
    parser.add_argument('--input', '-i', 
                        default="tag-list.txt",
                        help='入力ファイルパス (デフォルト: tag-list.txt)')
    
    parser.add_argument('--output', '-o', 
                        default=os.path.join("data", "processed", "jp_tags_new.json"),
                        help='出力JSONファイルパス (デフォルト: data/processed/jp_tags_new.json)')
    
    parser.add_argument('--base-dir', '-b', 
                        default=os.path.join("data", "raw", "wikidot_sources", "scp-jp"),
                        help='ファイルパスの基準ディレクトリ (デフォルト: data/raw/wikidot_sources/scp-jp)')
    
    parser.add_argument('--log-level', '-l',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default='INFO',
                        help='ログレベル (デフォルト: INFO)')
    
    parser.add_argument('--log-file', '-f',
                        help='ログファイルパス (指定しない場合はコンソールのみ)')
    
    args = parser.parse_args()
    
    # ログレベルの変換
    log_level = LogLevel(args.log_level)
    
    # 解析実行
    success = parse_jp_tags(
        start_filepath=args.input,
        output_filepath=args.output,
        base_dir=args.base_dir,
        log_level=log_level,
        log_file=args.log_file
    )
    
    # 終了コード
    exit(0 if success else 1)

if __name__ == "__main__":
    main()