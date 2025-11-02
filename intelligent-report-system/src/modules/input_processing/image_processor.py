"""
Image Data Processor
Handles image files and OCR extraction
"""
import pytesseract
from PIL import Image
import cv2
import numpy as np
from pathlib import Path
from typing import Optional
import uuid

from src.modules.input_processing.models import (
    ImageData, ImageMetadata, SourceType, ProcessingStatus
)
from src.utils.logger import app_logger as logger
from src.config.settings import settings

class ImageDataProcessor:
    """Process image data and extract text"""
    
    def __init__(self):
        logger.info("Initializing ImageDataProcessor")
        
        # Set tesseract path if specified
        if settings.TESSERACT_PATH:
            pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH
        
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']
    
    def process_image(self, file_path: str, perform_ocr: bool = True) -> ImageData:
        """Process image file"""
        try:
            logger.info(f"Processing image file: {file_path}")
            
            # Generate unique ID
            data_id = f"img_{uuid.uuid4().hex[:8]}"
            
            # Open image
            image = Image.open(file_path)
            
            # Extract basic metadata
            width, height = image.size
            img_format = image.format
            
            # Perform OCR if enabled
            extracted_text = ""
            text_confidence = None
            has_text = False
            
            if perform_ocr:
                extracted_text, text_confidence = self._extract_text_ocr(image)
                has_text = len(extracted_text.strip()) > 0
            
            # Detect objects (simple implementation)
            detected_objects = self._detect_objects(file_path)
            
            # Create metadata
            metadata = ImageMetadata(
                width=width,
                height=height,
                format=img_format,
                has_text=has_text,
                text_confidence=text_confidence,
                detected_objects=detected_objects
            )
            
            # Create image data object
            image_data = ImageData(
                data_id=data_id,
                source_type=SourceType.IMAGE,
                source_path=file_path,
                image_path=file_path,
                processed_content=extracted_text,
                metadata=metadata,
                status=ProcessingStatus.COMPLETED,
                processing_steps=["load_image", "extract_metadata", "perform_ocr"]
            )
            
            logger.info(f"Successfully processed image: {width}x{height}, text_found={has_text}")
            return image_data
            
        except Exception as e:
            logger.error(f"Error processing image file: {str(e)}")
            return self._create_failed_result(file_path, str(e))
    
    def _extract_text_ocr(self, image: Image.Image) -> tuple[str, Optional[float]]:
        """Extract text from image using OCR"""
        try:
            # Convert PIL image to numpy array
            img_array = np.array(image)
            
            # Preprocess image for better OCR
            processed_img = self._preprocess_image(img_array)
            
            # Perform OCR with detailed output
            ocr_data = pytesseract.image_to_data(
                processed_img,
                lang=settings.OCR_LANGUAGE,
                output_type=pytesseract.Output.DICT
            )
            
            # Extract text and calculate average confidence
            texts = []
            confidences = []
            
            for i, conf in enumerate(ocr_data['conf']):
                if conf > 0:  # Valid detection
                    text = ocr_data['text'][i].strip()
                    if text:
                        texts.append(text)
                        confidences.append(conf)
            
            extracted_text = " ".join(texts)
            avg_confidence = np.mean(confidences) if confidences else 0.0
            
            logger.debug(f"OCR extracted {len(texts)} text blocks with avg confidence {avg_confidence:.2f}")
            
            return extracted_text, float(avg_confidence)
            
        except Exception as e:
            logger.error(f"Error in OCR extraction: {str(e)}")
            return "", None
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for better OCR results"""
        try:
            # Convert to grayscale if color
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Apply thresholding
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Denoise
            denoised = cv2.fastNlMeansDenoising(thresh)
            
            return denoised
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            return image
    
    def _detect_objects(self, file_path: str) -> list[str]:
        """
        Detect objects in image (simplified implementation)
        In production, use models like YOLO or ResNet
        """
        detected_objects = []
        
        try:
            # This is a placeholder for object detection
            # In a full implementation, you would use:
            # - Pre-trained models (YOLO, Faster R-CNN, etc.)
            # - Hugging Face transformers for image classification
            # - Cloud vision APIs
            
            # For now, we'll do basic image analysis
            image = cv2.imread(file_path)
            
            if image is None:
                return detected_objects
            
            # Basic analysis
            height, width = image.shape[:2]
            aspect_ratio = width / height
            
            # Simple heuristics (placeholder)
            if aspect_ratio > 1.5:
                detected_objects.append("landscape_orientation")
            elif aspect_ratio < 0.7:
                detected_objects.append("portrait_orientation")
            else:
                detected_objects.append("square_orientation")
            
            # Analyze brightness
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            avg_brightness = np.mean(gray)
            
            if avg_brightness > 200:
                detected_objects.append("bright_image")
            elif avg_brightness < 50:
                detected_objects.append("dark_image")
            
            logger.debug(f"Detected objects/properties: {detected_objects}")
            
        except Exception as e:
            logger.error(f"Error detecting objects: {str(e)}")
        
        return detected_objects
    
    def process_scanned_document(self, file_path: str) -> ImageData:
        """Process scanned document with enhanced OCR"""
        try:
            logger.info(f"Processing scanned document: {file_path}")
            
            # Process as image with OCR
            image_data = self.process_image(file_path, perform_ocr=True)
            
            # Update source type
            image_data.source_type = SourceType.SCANNED_DOC
            
            # Additional processing for documents
            if image_data.processed_content:
                # Structure the extracted text
                lines = image_data.processed_content.split('\n')
                structured_text = '\n'.join([line.strip() for line in lines if line.strip()])
                image_data.processed_content = structured_text
            
            return image_data
            
        except Exception as e:
            logger.error(f"Error processing scanned document: {str(e)}")
            return self._create_failed_result(file_path, str(e))
    
    def _create_failed_result(self, source_path: str, error: str) -> ImageData:
        """Create a failed processing result"""
        return ImageData(
            data_id=f"img_{uuid.uuid4().hex[:8]}",
            source_type=SourceType.IMAGE,
            source_path=source_path,
            image_path=source_path,
            processed_content="",
            status=ProcessingStatus.FAILED,
            errors=[error]
        )
    
    def process(self, file_path: str, is_scanned_doc: bool = False) -> ImageData:
        """Main processing method"""
        if is_scanned_doc:
            return self.process_scanned_document(file_path)
        else:
            return self.process_image(file_path)