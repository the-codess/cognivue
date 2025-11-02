"""
Text Data Processor
Handles text documents, PDFs, Word files, and plain text
"""
import spacy
from pathlib import Path
from typing import List, Optional
import uuid
import re
from docx import Document
import PyPDF2
from transformers import pipeline

from src.modules.input_processing.models import (
    TextData, TextMetadata, Entity, Sentiment, SourceType, ProcessingStatus
)
from src.utils.logger import app_logger as logger
from src.config.settings import settings

class TextDataProcessor:
    """Process text data from various sources"""
    
    def __init__(self):
        logger.info("Initializing TextDataProcessor")
        
        # Load spaCy model
        try:
            self.nlp = spacy.load(settings.SPACY_MODEL)
            logger.info(f"Loaded spaCy model: {settings.SPACY_MODEL}")
        except OSError:
            logger.warning(f"spaCy model {settings.SPACY_MODEL} not found. Downloading...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", settings.SPACY_MODEL])
            self.nlp = spacy.load(settings.SPACY_MODEL)
        
        # Load sentiment analysis pipeline
        try:
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1  # CPU
            )
            logger.info("Loaded sentiment analysis model")
        except Exception as e:
            logger.warning(f"Could not load sentiment analyzer: {str(e)}")
            self.sentiment_analyzer = None
        
        self.supported_formats = ['.txt', '.pdf', '.docx', '.doc']
    
    def process_text_file(self, file_path: str) -> TextData:
        """Process plain text file"""
        try:
            logger.info(f"Processing text file: {file_path}")
            
            # Read text
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            return self._process_text_content(text, file_path, SourceType.TXT)
            
        except Exception as e:
            logger.error(f"Error processing text file: {str(e)}")
            return self._create_failed_result(file_path, SourceType.TXT, str(e))
    
    def process_pdf(self, file_path: str) -> TextData:
        """Process PDF file"""
        try:
            logger.info(f"Processing PDF file: {file_path}")
            
            text = ""
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                num_pages = len(pdf_reader.pages)
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n\n"
            
            return self._process_text_content(text, file_path, SourceType.PDF)
            
        except Exception as e:
            logger.error(f"Error processing PDF file: {str(e)}")
            return self._create_failed_result(file_path, SourceType.PDF, str(e))
    
    def process_docx(self, file_path: str) -> TextData:
        """Process Word document"""
        try:
            logger.info(f"Processing DOCX file: {file_path}")
            
            doc = Document(file_path)
            text = "\n\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            return self._process_text_content(text, file_path, SourceType.DOCX)
            
        except Exception as e:
            logger.error(f"Error processing DOCX file: {str(e)}")
            return self._create_failed_result(file_path, SourceType.DOCX, str(e))
    
    def _process_text_content(self, text: str, source_path: str, source_type: SourceType) -> TextData:
        """Process text content and extract features"""
        try:
            # Generate unique ID
            data_id = f"text_{uuid.uuid4().hex[:8]}"
            
            # Clean text
            cleaned_text = self._clean_text(text)
            
            # Extract entities
            entities = self._extract_entities(cleaned_text)
            
            # Analyze sentiment
            sentiment = self._analyze_sentiment(cleaned_text)
            
            # Extract key phrases
            key_phrases = self._extract_key_phrases(cleaned_text)
            
            # Count words and sentences
            word_count = len(cleaned_text.split())
            sentence_count = len(re.split(r'[.!?]+', cleaned_text))
            
            # Create metadata
            metadata = TextMetadata(
                word_count=word_count,
                sentence_count=sentence_count,
                language="en",  # Default, can be detected
                entities=entities,
                sentiment=sentiment,
                topics=[],  # Will be filled by topic modeling
                key_phrases=key_phrases
            )
            
            # Create text data object
            text_data = TextData(
                data_id=data_id,
                source_type=source_type,
                source_path=source_path,
                raw_content=text,
                processed_content=cleaned_text,
                metadata=metadata,
                status=ProcessingStatus.COMPLETED,
                processing_steps=[
                    "clean_text",
                    "extract_entities",
                    "analyze_sentiment",
                    "extract_key_phrases"
                ]
            )
            
            logger.info(f"Successfully processed text with {word_count} words and {len(entities)} entities")
            return text_data
            
        except Exception as e:
            logger.error(f"Error processing text content: {str(e)}")
            return self._create_failed_result(source_path, source_type, str(e))
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,!?;:\-\'\"()]', '', text)
        return text.strip()
    
    def _extract_entities(self, text: str) -> List[Entity]:
        """Extract named entities using spaCy"""
        entities = []
        
        try:
            # Limit text length for processing
            if len(text) > settings.MAX_TEXT_LENGTH:
                text = text[:settings.MAX_TEXT_LENGTH]
            
            doc = self.nlp(text)
            
            for ent in doc.ents:
                entity = Entity(
                    text=ent.text,
                    label=ent.label_,
                    start=ent.start_char,
                    end=ent.end_char,
                    confidence=None  # spaCy doesn't provide confidence scores by default
                )
                entities.append(entity)
            
            logger.debug(f"Extracted {len(entities)} entities")
            
        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
        
        return entities
    
    def _analyze_sentiment(self, text: str) -> Optional[Sentiment]:
        """Analyze sentiment of text"""
        if not self.sentiment_analyzer:
            return None
        
        try:
            # Limit text length for sentiment analysis
            max_length = 512
            text_sample = text[:max_length] if len(text) > max_length else text
            
            result = self.sentiment_analyzer(text_sample)[0]
            
            sentiment = Sentiment(
                label=result['label'].lower(),
                score=result['score']
            )
            
            logger.debug(f"Sentiment: {sentiment.label} ({sentiment.score:.2f})")
            return sentiment
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return None
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases using noun chunks"""
        key_phrases = []
        
        try:
            # Limit text length
            if len(text) > settings.MAX_TEXT_LENGTH:
                text = text[:settings.MAX_TEXT_LENGTH]
            
            doc = self.nlp(text)
            
            # Extract noun chunks
            for chunk in doc.noun_chunks:
                if len(chunk.text.split()) >= 2:  # Multi-word phrases
                    key_phrases.append(chunk.text)
            
            # Remove duplicates and limit to top phrases
            key_phrases = list(set(key_phrases))[:20]
            
            logger.debug(f"Extracted {len(key_phrases)} key phrases")
            
        except Exception as e:
            logger.error(f"Error extracting key phrases: {str(e)}")
        
        return key_phrases
    
    def _create_failed_result(self, source_path: str, source_type: SourceType, error: str) -> TextData:
        """Create a failed processing result"""
        return TextData(
            data_id=f"text_{uuid.uuid4().hex[:8]}",
            source_type=source_type,
            source_path=source_path,
            processed_content="",
            status=ProcessingStatus.FAILED,
            errors=[error]
        )
    
    def process(self, file_path: str) -> TextData:
        """Main processing method that routes to appropriate handler"""
        path = Path(file_path)
        suffix = path.suffix.lower()
        
        if suffix == '.txt':
            return self.process_text_file(file_path)
        elif suffix == '.pdf':
            return self.process_pdf(file_path)
        elif suffix in ['.docx', '.doc']:
            return self.process_docx(file_path)
        else:
            logger.error(f"Unsupported file format: {suffix}")
            return self._create_failed_result(
                file_path,
                SourceType.TXT,
                f"Unsupported file format: {suffix}"
            )