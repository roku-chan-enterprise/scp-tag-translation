"""
SCP財団タグリスト解析システム

SCP財団日本語Wikiのタグリスト（Wikidotソース）を解析し、
各タグに関する情報を網羅的に抽出し、構造化されたJSONファイルとして出力するシステム。
"""

from .models import (
    LogLevel, ErrorType, Restriction, RelatedPage, RelatedTag,
    SourceLocation, Meta, Tag, ParserError
)
from .logger import Logger
from .error_handler import ErrorHandler
from .source_loader import SourceLoader
from .lexer import Lexer
from .heading_parser import HeadingParser
from .restr_icon_extractor import RestrIconExtractor
from .basic_field_parser import BasicFieldParser
from .wikidot_link_scanner import WikidotLinkScanner
from .tag_mention_miner import TagMentionMiner
from .page_type_heuristics import PageTypeHeuristics
from .footnote_stripper import FootnoteStripper
from .plain_text_stripper import PlainTextStripper
from .desc_analyzer import DescAnalyzer
from .emitter import Emitter
from .json_dumper import JSONDumper
from .main import parse_jp_tags, main

__version__ = "0.1.0"
__author__ = "SCP-JP"
__all__ = [
    "LogLevel", "ErrorType", "Restriction", "RelatedPage", "RelatedTag",
    "SourceLocation", "Meta", "Tag", "ParserError",
    "Logger", "ErrorHandler",
    "SourceLoader", "Lexer", "HeadingParser",
    "RestrIconExtractor", "BasicFieldParser",
    "WikidotLinkScanner", "TagMentionMiner", "PageTypeHeuristics",
    "FootnoteStripper", "PlainTextStripper", "DescAnalyzer",
    "Emitter", "JSONDumper",
    "parse_jp_tags", "main"
]