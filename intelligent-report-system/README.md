# Intelligent Report Generation System - POC

A context-aware intelligent report generation system with multi-modal analytics and explainable AI.

## Project Overview

This system addresses critical limitations in contemporary business intelligence platforms by integrating:
- **Multi-modal data processing** (structured, text, image, conversational)
- **Role-aware insight orchestration** 
- **Explainable AI mechanisms**
- **Conversational adaptive interfaces**

## Current Status: Module 1 Complete

✅ **Module 1: Multi-Modal Input Processing Layer** - COMPLETE
- Structured data processing (CSV, Excel)
- Text document processing (TXT, PDF, DOCX)
- Image processing with OCR
- Entity extraction and sentiment analysis
- Batch processing capabilities

🔄 **Module 2: Role-Context Analyzer** - Coming Next
🔄 **Module 3: Insight Generation & Explanation Engine** - Pending
🔄 **Module 4: Conversational Interface Layer** - Pending
🔄 **Module 5: Feedback & Learning System** - Pending

## Technology Stack

### Core Technologies
- **Python 3.10+**
- **FastAPI** - API framework
- **Pandas/NumPy** - Data processing

### NLP & ML
- **spaCy** - Entity recognition
- **Transformers** - Sentiment analysis
- **sentence-transformers** - Embeddings
- **BERTopic** - Topic modeling

### Document Processing
- **PyPDF2** - PDF extraction
- **python-docx** - Word documents
- **pytesseract** - OCR

### LLM Integration (Coming)
- **Ollama** - Local LLM inference
- **LangChain** - LLM orchestration

## Installation

### Prerequisites
- Python 3.10 or higher
- Tesseract OCR (for image processing)

### Step 1: Clone the repository
```bash
git clone <repository-url>
cd intelligent-report-system
```

### Step 2: Create virtual environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download spaCy model
```bash
python -m spacy download en_core_web_sm
```

### Step 5: Install Tesseract OCR

**Windows:**
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and note the installation path
3. Update `.env` with the path

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

### Step 6: Configure environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running Module 1

### Quick Test
```bash
python test_module1.py
```

This will:
1. Generate sample data files
2. Process structured data (CSV)
3. Process text documents (TXT)
4. Process images with OCR (PNG)
5. Run batch processing
6. Display results and statistics

### Using the Module Programmatically

```python
from src.modules.input_processing.processor import InputProcessor

# Initialize processor
processor = InputProcessor()

# Process a single file
result = processor.process_file('data/sample/sales_data.csv')

print(f"Status: {result.status}")
print(f"Data ID: {result.data_id}")
print(f"Metadata: {result.metadata}")

# Process multiple files
batch = processor.process_batch([
    'data/sample/sales_data.csv',
    'data/sample/financial_report.txt',
    'data/sample/sample_invoice.png'
])

print(f"Processed {batch.total_count} files")
```

### Processing Different Data Types

**Structured Data (CSV/Excel):**
```python
from src.modules.input_processing.structured_processor import StructuredDataProcessor

processor = StructuredDataProcessor()
result = processor.process_csv('sales_data.csv')
print(f"Rows: {result.metadata.row_count}")
print(f"Columns: {result.metadata.columns}")
```

**Text Documents:**
```python
from src.modules.input_processing.text_processor import TextDataProcessor

processor = TextDataProcessor()
result = processor.process_pdf('report.pdf')
print(f"Entities: {result.metadata.entities}")
print(f"Sentiment: {result.metadata.sentiment}")
```

**Images with OCR:**
```python
from src.modules.input_processing.image_processor import ImageDataProcessor

processor = ImageDataProcessor()
result = processor.process_image('invoice.png')
print(f"Extracted text: {result.processed_content}")
print(f"Confidence: {result.metadata.text_confidence}")
```

## Project Structure

```
intelligent-report-system/
├── src/
│   ├── modules/
│   │   ├── input_processing/         # Module 1 - COMPLETE
│   │   │   ├── __init__.py
│   │   │   ├── models.py            # Data models
│   │   │   ├── processor.py         # Main coordinator
│   │   │   ├── structured_processor.py
│   │   │   ├── text_processor.py
│   │   │   └── image_processor.py
│   │   ├── role_context/            # Module 2 - NEXT
│   │   ├── insight_generation/      # Module 3
│   │   ├── conversational_interface/# Module 4
│   │   └── feedback_learning/       # Module 5
│   ├── config/
│   │   └── settings.py              # Configuration
│   └── utils/
│       ├── logger.py                # Logging utilities
│       └── sample_data_generator.py # Test data generation
├── data/
│   ├── raw/                         # Raw input data
│   ├── processed/                   # Processed data
│   └── sample/                      # Sample/test data
├── logs/                            # Application logs
├── tests/                           # Unit tests
├── requirements.txt                 # Python dependencies
├── test_module1.py                  # Module 1 test script
├── .env.example                     # Environment template
└── README.md                        # This file
```

## Module 1 Features

### Supported File Formats
- **Structured:** CSV, Excel (XLSX, XLS)
- **Text:** TXT, PDF, DOCX
- **Images:** JPG, PNG, BMP, TIFF, GIF

### Processing Capabilities

**For Structured Data:**
- Automatic schema detection
- Summary statistics
- Null value analysis
- Data type inference

**For Text Documents:**
- Named Entity Recognition (NER)
- Sentiment analysis
- Key phrase extraction
- Document metadata

**For Images:**
- OCR text extraction
- Image metadata
- Text confidence scoring
- Basic object detection

### Data Models

All processed data follows a consistent schema:
- `data_id`: Unique identifier
- `modality`: Type of data (structured/text/image)
- `source_type`: Original format
- `processed_content`: Cleaned/extracted content
- `metadata`: Type-specific metadata
- `processing_steps`: Audit trail
- `status`: Processing status

## Configuration

Key settings in `.env`:

```bash
# LLM Settings (for future modules)
LLM_MODEL=llama2
LLM_BASE_URL=http://localhost:11434

# OCR Settings
TESSERACT_PATH=/usr/bin/tesseract
OCR_LANGUAGE=eng

# NLP Settings
SPACY_MODEL=en_core_web_sm

# Logging
LOG_LEVEL=INFO
```

## Logging

Logs are saved in the `logs/` directory:
- `app_YYYY-MM-DD.log` - All logs
- `errors_YYYY-MM-DD.log` - Errors only

View logs in real-time:
```bash
tail -f logs/app_*.log
```

## Testing

### Run Module 1 Tests
```bash
python test_module1.py
```

### Run Unit Tests (when available)
```bash
pytest tests/
```

### Generate Coverage Report
```bash
pytest --cov=src tests/
```

## Sample Output

When you run the test script, you'll see:

```
================================================================================
  MODULE 1: MULTI-MODAL INPUT PROCESSING - TEST SUITE
================================================================================

✓ Structured Data Processing: WORKING
✓ Text Data Processing: WORKING
✓ Image Data Processing (OCR): WORKING
✓ Batch Processing: WORKING
✓ Metadata Extraction: WORKING
✓ Entity Recognition: WORKING
✓ Sentiment Analysis: WORKING

Modality breakdown:
  structured: 1 files
  text: 2 files
  image: 1 files
```

## Troubleshooting

### Common Issues

**Issue: spaCy model not found**
```bash
python -m spacy download en_core_web_sm
```

**Issue: Tesseract not found**
- Ensure Tesseract is installed
- Update `TESSERACT_PATH` in `.env`

**Issue: Out of memory during processing**
- Reduce `BATCH_SIZE` in settings
- Process fewer files at once
- Increase system RAM

**Issue: Slow text processing**
- The first run downloads ML models
- Subsequent runs will be faster
- Consider using smaller spaCy models

## Next Steps

1. ✅ Complete Module 1 testing
2. 🔄 Develop Module 2: Role-Context Analyzer
   - Define organizational role ontology
   - Implement role-to-insight mapping
   - Create role-based filters
3. 🔄 Develop Module 3: Insight Generation
   - Statistical analysis engine
   - Explainability framework
   - Natural language generation
4. 🔄 Develop Module 4: Conversational Interface
   - LLM integration with Ollama
   - RAG implementation
   - Query processing
5. 🔄 Develop Module 5: Feedback & Learning
   - Feedback collection
   - Adaptive learning algorithms
   - Performance monitoring

## Contributing

This is an academic project. For questions or suggestions, please contact the project team.

## License

[Your License Here]

## Acknowledgments

- spaCy for NLP capabilities
- Hugging Face for transformer models
- Tesseract OCR for text extraction
- Open-source community for tools and libraries

---

**Project Status:** Module 1 Complete ✅ | In Active Development 🔄

Last Updated: October 31, 2024