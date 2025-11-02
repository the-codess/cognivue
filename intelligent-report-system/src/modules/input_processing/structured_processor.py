"""
Structured Data Processor
Handles CSV, Excel, and database data
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List
from sqlalchemy import create_engine, inspect
import uuid

from src.modules.input_processing.models import (
    StructuredData, StructuredMetadata, SourceType, ProcessingStatus
)
from src.utils.logger import app_logger as logger
from src.config.settings import settings

class StructuredDataProcessor:
    """Process structured data from various sources"""
    
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.xls']
        logger.info("StructuredDataProcessor initialized")
    
    def process_csv(self, file_path: str) -> StructuredData:
        """Process CSV file"""
        try:
            logger.info(f"Processing CSV file: {file_path}")
            
            # Read CSV
            df = pd.read_csv(file_path)
            
            # Generate unique ID
            data_id = f"struct_{uuid.uuid4().hex[:8]}"
            
            # Extract metadata
            metadata = self._extract_metadata(df)
            
            # Convert to dict for storage
            processed_content = {
                'data': df.to_dict(orient='records'),
                'columns': df.columns.tolist(),
                'index': df.index.tolist()
            }
            
            # Create structured data object
            structured_data = StructuredData(
                data_id=data_id,
                source_type=SourceType.CSV,
                source_path=file_path,
                processed_content=processed_content,
                metadata=metadata,
                status=ProcessingStatus.COMPLETED,
                processing_steps=["read_csv", "extract_metadata", "convert_to_dict"]
            )
            
            logger.info(f"Successfully processed CSV with {len(df)} rows and {len(df.columns)} columns")
            return structured_data
            
        except Exception as e:
            logger.error(f"Error processing CSV file: {str(e)}")
            return StructuredData(
                data_id=f"struct_{uuid.uuid4().hex[:8]}",
                source_type=SourceType.CSV,
                source_path=file_path,
                processed_content={},
                status=ProcessingStatus.FAILED,
                errors=[str(e)]
            )
    
    def process_excel(self, file_path: str, sheet_name: Optional[str] = None) -> StructuredData:
        """Process Excel file"""
        try:
            logger.info(f"Processing Excel file: {file_path}")
            
            # Read Excel
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                df = pd.read_excel(file_path)
            
            # Generate unique ID
            data_id = f"struct_{uuid.uuid4().hex[:8]}"
            
            # Extract metadata
            metadata = self._extract_metadata(df)
            
            # Convert to dict for storage
            processed_content = {
                'data': df.to_dict(orient='records'),
                'columns': df.columns.tolist(),
                'index': df.index.tolist(),
                'sheet_name': sheet_name
            }
            
            # Create structured data object
            structured_data = StructuredData(
                data_id=data_id,
                source_type=SourceType.EXCEL,
                source_path=file_path,
                processed_content=processed_content,
                metadata=metadata,
                status=ProcessingStatus.COMPLETED,
                processing_steps=["read_excel", "extract_metadata", "convert_to_dict"]
            )
            
            logger.info(f"Successfully processed Excel with {len(df)} rows and {len(df.columns)} columns")
            return structured_data
            
        except Exception as e:
            logger.error(f"Error processing Excel file: {str(e)}")
            return StructuredData(
                data_id=f"struct_{uuid.uuid4().hex[:8]}",
                source_type=SourceType.EXCEL,
                source_path=file_path,
                processed_content={},
                status=ProcessingStatus.FAILED,
                errors=[str(e)]
            )
    
    def process_database_query(self, query: str, connection_string: str) -> StructuredData:
        """Process data from database query"""
        try:
            logger.info("Processing database query")
            
            # Create engine
            engine = create_engine(connection_string)
            
            # Execute query
            df = pd.read_sql(query, engine)
            
            # Generate unique ID
            data_id = f"struct_{uuid.uuid4().hex[:8]}"
            
            # Extract metadata
            metadata = self._extract_metadata(df)
            
            # Convert to dict for storage
            processed_content = {
                'data': df.to_dict(orient='records'),
                'columns': df.columns.tolist(),
                'index': df.index.tolist(),
                'query': query
            }
            
            # Create structured data object
            structured_data = StructuredData(
                data_id=data_id,
                source_type=SourceType.DATABASE,
                source_path=connection_string,
                processed_content=processed_content,
                metadata=metadata,
                status=ProcessingStatus.COMPLETED,
                processing_steps=["connect_db", "execute_query", "extract_metadata"]
            )
            
            logger.info(f"Successfully processed database query with {len(df)} rows")
            return structured_data
            
        except Exception as e:
            logger.error(f"Error processing database query: {str(e)}")
            return StructuredData(
                data_id=f"struct_{uuid.uuid4().hex[:8]}",
                source_type=SourceType.DATABASE,
                source_path=connection_string,
                processed_content={},
                status=ProcessingStatus.FAILED,
                errors=[str(e)]
            )
    
    def _extract_metadata(self, df: pd.DataFrame) -> StructuredMetadata:
        """Extract metadata from DataFrame"""
        try:
            # Basic info
            row_count = len(df)
            column_count = len(df.columns)
            columns = df.columns.tolist()
            
            # Data types
            data_types = {col: str(dtype) for col, dtype in df.dtypes.items()}
            
            # Null counts
            null_counts = df.isnull().sum().to_dict()
            
            # Summary statistics for numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            summary_stats = {}
            
            for col in numeric_cols:
                summary_stats[col] = {
                    'mean': float(df[col].mean()) if not pd.isna(df[col].mean()) else None,
                    'median': float(df[col].median()) if not pd.isna(df[col].median()) else None,
                    'std': float(df[col].std()) if not pd.isna(df[col].std()) else None,
                    'min': float(df[col].min()) if not pd.isna(df[col].min()) else None,
                    'max': float(df[col].max()) if not pd.isna(df[col].max()) else None,
                    'q25': float(df[col].quantile(0.25)) if not pd.isna(df[col].quantile(0.25)) else None,
                    'q75': float(df[col].quantile(0.75)) if not pd.isna(df[col].quantile(0.75)) else None,
                }
            
            metadata = StructuredMetadata(
                row_count=row_count,
                column_count=column_count,
                columns=columns,
                data_types=data_types,
                null_counts=null_counts,
                summary_stats=summary_stats
            )
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error extracting metadata: {str(e)}")
            return StructuredMetadata(
                row_count=len(df),
                column_count=len(df.columns),
                columns=df.columns.tolist(),
                data_types={},
                null_counts={}
            )
    
    def process(self, file_path: str, **kwargs) -> StructuredData:
        """Main processing method that routes to appropriate handler"""
        path = Path(file_path)
        suffix = path.suffix.lower()
        
        if suffix == '.csv':
            return self.process_csv(file_path)
        elif suffix in ['.xlsx', '.xls']:
            return self.process_excel(file_path, kwargs.get('sheet_name'))
        else:
            logger.error(f"Unsupported file format: {suffix}")
            return StructuredData(
                data_id=f"struct_{uuid.uuid4().hex[:8]}",
                source_type=SourceType.CSV,
                source_path=file_path,
                processed_content={},
                status=ProcessingStatus.FAILED,
                errors=[f"Unsupported file format: {suffix}"]
            )