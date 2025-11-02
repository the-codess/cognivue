"""
Data models for input processing module
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime
from enum import Enum

class DataModality(str, Enum):
    """Supported data modalities"""
    STRUCTURED = "structured"
    TEXT = "text"
    IMAGE = "image"
    CONVERSATION = "conversation"

class SourceType(str, Enum):
    """Source type for data"""
    DATABASE = "database"
    CSV = "csv"
    EXCEL = "excel"
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    EMAIL = "email"
    IMAGE = "image"
    SCANNED_DOC = "scanned_document"
    AUDIO = "audio"
    TRANSCRIPT = "transcript"

class ProcessingStatus(str, Enum):
    """Processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Entity(BaseModel):
    """Named entity extracted from text"""
    text: str
    label: str
    start: int
    end: int
    confidence: Optional[float] = None

class Sentiment(BaseModel):
    """Sentiment analysis result"""
    label: str  # positive, negative, neutral
    score: float
    
class Topic(BaseModel):
    """Topic modeling result"""
    topic_id: int
    topic_name: str
    keywords: List[str]
    probability: float

class TextMetadata(BaseModel):
    """Metadata for processed text"""
    word_count: int
    sentence_count: int
    language: str
    entities: List[Entity] = []
    sentiment: Optional[Sentiment] = None
    topics: List[Topic] = []
    key_phrases: List[str] = []

class ImageMetadata(BaseModel):
    """Metadata for processed images"""
    width: int
    height: int
    format: str
    has_text: bool
    text_confidence: Optional[float] = None
    detected_objects: List[str] = []

class StructuredMetadata(BaseModel):
    """Metadata for structured data"""
    row_count: int
    column_count: int
    columns: List[str]
    data_types: Dict[str, str]
    null_counts: Dict[str, int]
    summary_stats: Optional[Dict[str, Any]] = None

class ProcessedData(BaseModel):
    """Base model for processed data"""
    data_id: str = Field(description="Unique identifier for the data")
    modality: DataModality
    source_type: SourceType
    source_path: str
    processed_at: datetime = Field(default_factory=datetime.now)
    status: ProcessingStatus = ProcessingStatus.COMPLETED
    
    # Content
    raw_content: Optional[str] = None
    processed_content: Any = None
    
    # Metadata
    metadata: Optional[Dict[str, Any]] = None
    
    # Embeddings
    embeddings: Optional[List[float]] = None
    
    # Provenance
    processing_steps: List[str] = []
    errors: List[str] = []

class StructuredData(ProcessedData):
    """Model for structured data"""
    modality: Literal[DataModality.STRUCTURED] = DataModality.STRUCTURED
    processed_content: Dict[str, Any]  # DataFrame as dict
    metadata: Optional[StructuredMetadata] = None

class TextData(ProcessedData):
    """Model for text data"""
    modality: Literal[DataModality.TEXT] = DataModality.TEXT
    processed_content: str
    metadata: Optional[TextMetadata] = None

class ImageData(ProcessedData):
    """Model for image data"""
    modality: Literal[DataModality.IMAGE] = DataModality.IMAGE
    processed_content: str  # Extracted text or description
    metadata: Optional[ImageMetadata] = None
    image_path: str

class ConversationData(ProcessedData):
    """Model for conversational data"""
    modality: Literal[DataModality.CONVERSATION] = DataModality.CONVERSATION
    processed_content: List[Dict[str, str]]  # List of speaker: message
    metadata: Optional[TextMetadata] = None
    speakers: List[str] = []
    duration: Optional[float] = None

class DataBatch(BaseModel):
    """Batch of processed data"""
    batch_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    data_items: List[ProcessedData]
    total_count: int
    modality_counts: Dict[DataModality, int] = {}
    
class ProcessingConfig(BaseModel):
    """Configuration for data processing"""
    extract_entities: bool = True
    analyze_sentiment: bool = True
    extract_topics: bool = True
    generate_embeddings: bool = True
    ocr_enabled: bool = True
    max_text_length: int = 100000
    batch_size: int = 32