"""
Main Input Processing Coordinator
Orchestrates all data processors
"""
from pathlib import Path
from typing import Union, List
import uuid
from datetime import datetime

from src.modules.input_processing.structured_processor import StructuredDataProcessor
from src.modules.input_processing.text_processor import TextDataProcessor
from src.modules.input_processing.image_processor import ImageDataProcessor
from src.modules.input_processing.models import (
    ProcessedData, DataBatch, DataModality, ProcessingConfig
)
from src.utils.logger import app_logger as logger

class InputProcessor:
    """Main coordinator for all input processing"""
    
    def __init__(self, config: ProcessingConfig = None):
        logger.info("Initializing InputProcessor")
        
        self.config = config or ProcessingConfig()
        
        # Initialize sub-processors
        self.structured_processor = StructuredDataProcessor()
        self.text_processor = TextDataProcessor()
        self.image_processor = ImageDataProcessor()
        
        # File extension mappings
        self.extension_map = {
            'structured': ['.csv', '.xlsx', '.xls'],
            'text': ['.txt', '.pdf', '.docx', '.doc'],
            'image': ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']
        }
        
        logger.info("InputProcessor initialized successfully")
    
    def process_file(self, file_path: str, **kwargs) -> ProcessedData:
        """Process a single file based on its type"""
        try:
            path = Path(file_path)
            
            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            suffix = path.suffix.lower()
            logger.info(f"Processing file: {file_path} (type: {suffix})")
            
            # Route to appropriate processor
            if suffix in self.extension_map['structured']:
                return self.structured_processor.process(file_path, **kwargs)
            
            elif suffix in self.extension_map['text']:
                return self.text_processor.process(file_path)
            
            elif suffix in self.extension_map['image']:
                is_scanned = kwargs.get('is_scanned_doc', False)
                return self.image_processor.process(file_path, is_scanned)
            
            else:
                raise ValueError(f"Unsupported file type: {suffix}")
        
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            raise
    
    def process_directory(self, directory_path: str, recursive: bool = False) -> DataBatch:
        """Process all supported files in a directory"""
        try:
            logger.info(f"Processing directory: {directory_path} (recursive={recursive})")
            
            dir_path = Path(directory_path)
            if not dir_path.is_dir():
                raise NotADirectoryError(f"Not a directory: {directory_path}")
            
            # Collect all supported files
            pattern = "**/*" if recursive else "*"
            all_files = list(dir_path.glob(pattern))
            
            # Filter supported files
            supported_extensions = (
                self.extension_map['structured'] +
                self.extension_map['text'] +
                self.extension_map['image']
            )
            
            files_to_process = [
                f for f in all_files 
                if f.is_file() and f.suffix.lower() in supported_extensions
            ]
            
            logger.info(f"Found {len(files_to_process)} supported files")
            
            # Process each file
            processed_items = []
            for file_path in files_to_process:
                try:
                    result = self.process_file(str(file_path))
                    processed_items.append(result)
                except Exception as e:
                    logger.error(f"Failed to process {file_path}: {str(e)}")
                    continue
            
            # Create batch
            batch = self._create_batch(processed_items)
            
            logger.info(f"Successfully processed {len(processed_items)} files")
            return batch
        
        except Exception as e:
            logger.error(f"Error processing directory: {str(e)}")
            raise
    
    def process_batch(self, file_paths: List[str]) -> DataBatch:
        """Process a batch of files"""
        try:
            logger.info(f"Processing batch of {len(file_paths)} files")
            
            processed_items = []
            for file_path in file_paths:
                try:
                    result = self.process_file(file_path)
                    processed_items.append(result)
                except Exception as e:
                    logger.error(f"Failed to process {file_path}: {str(e)}")
                    continue
            
            batch = self._create_batch(processed_items)
            
            logger.info(f"Successfully processed {len(processed_items)} files in batch")
            return batch
        
        except Exception as e:
            logger.error(f"Error processing batch: {str(e)}")
            raise
    
    def _create_batch(self, processed_items: List[ProcessedData]) -> DataBatch:
        """Create a DataBatch from processed items"""
        batch_id = f"batch_{uuid.uuid4().hex[:8]}"
        
        # Count modalities
        modality_counts = {}
        for item in processed_items:
            modality = item.modality
            modality_counts[modality] = modality_counts.get(modality, 0) + 1
        
        batch = DataBatch(
            batch_id=batch_id,
            created_at=datetime.now(),
            data_items=processed_items,
            total_count=len(processed_items),
            modality_counts=modality_counts
        )
        
        return batch
    
    def get_supported_formats(self) -> dict:
        """Get all supported file formats"""
        return self.extension_map
    
    def validate_file(self, file_path: str) -> tuple[bool, str]:
        """Validate if a file can be processed"""
        try:
            path = Path(file_path)
            
            if not path.exists():
                return False, "File does not exist"
            
            if not path.is_file():
                return False, "Path is not a file"
            
            suffix = path.suffix.lower()
            all_supported = (
                self.extension_map['structured'] +
                self.extension_map['text'] +
                self.extension_map['image']
            )
            
            if suffix not in all_supported:
                return False, f"Unsupported file type: {suffix}"
            
            return True, "File is valid"
        
        except Exception as e:
            return False, f"Validation error: {str(e)}"