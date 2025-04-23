from pydantic import BaseModel, Field, validator
from typing import List, Optional, NamedTuple
from enum import Enum

# ログレベルの定義
class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

# エラータイプの定義
class ErrorType(str, Enum):
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    CIRCULAR_REFERENCE = "CIRCULAR_REFERENCE"
    PARSE_ERROR = "PARSE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    SERIALIZATION_ERROR = "SERIALIZATION_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"

class Restriction(NamedTuple):
    icon: str
    meaning: str

class RelatedPage(BaseModel):
    slug: str
    display_name: Optional[str] = None

class RelatedTag(BaseModel):
    slug: str
    relation_type: str

class SourceLocation(BaseModel):
    file: str
    line: int

class Meta(BaseModel):
    related_pages: List[RelatedPage] = Field(default_factory=list)
    related_tags: List[RelatedTag] = Field(default_factory=list)
    target_page_types: List[str] = Field(default_factory=list)
    footnotes: List[str] = Field(default_factory=list)
    other_notes: List[str] = Field(default_factory=list)

class Tag(BaseModel):
    slug: str
    name_jp: str
    name_en: Optional[str] = None
    description_raw: str
    description_plain: str
    category_path: List[str]
    restrictions: List[Restriction] = Field(default_factory=list)
    meta: Meta = Field(default_factory=Meta)
    source_location: SourceLocation
    
    # バリデーション
    @validator('slug')
    def slug_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('スラッグは空であってはなりません')
        return v
    
    @validator('name_jp')
    def name_jp_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('日本語名は空であってはなりません')
        return v
    
    @validator('category_path')
    def category_path_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('カテゴリパスは空であってはなりません')
        return v

class ParserError(BaseModel):
    error_type: ErrorType
    message: str
    source_file: Optional[str] = None
    line_number: Optional[int] = None
    details: Optional[dict] = None