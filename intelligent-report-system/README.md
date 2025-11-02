# 🎯 Cognivue: Intelligent Role-Based Report Generation System

> A context-aware intelligent report generation system with multi-modal analytics, role-based insights, and conversational AI interface.

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Module Documentation](#module-documentation)
- [Recent Fixes](#recent-fixes)
- [Troubleshooting](#troubleshooting)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Academic Context](#academic-context)

---

## 🎯 Overview

This system addresses critical limitations in contemporary business intelligence platforms by providing **intelligent, role-aware report generation** that automatically adapts content, visualizations, and insights based on the recipient's organizational role and decision-making context.

### Problem Statement

Organizations generate vast amounts of data, yet transforming this raw data into actionable insights remains time-intensive and often requires specialized analytical skills. Different stakeholders require different perspectives on the same underlying data—a CFO needs enterprise-wide financial trends, while a regional manager requires granular, geography-specific operational details.

### Solution

An **AI-powered system** that:
- 📊 Automatically processes multi-modal data (structured, text, images)
- 🎭 Generates role-specific insights and visualizations
- 💬 Provides conversational interface for data exploration
- 🧠 Learns from user feedback to improve over time
- 🔍 Offers explainable AI for transparency

---

## ✨ Key Features

### 🔄 Multi-Modal Data Processing
- **Structured Data**: CSV, Excel (XLSX, XLS) with automatic schema detection
- **Text Documents**: PDF, DOCX, TXT with NLP analysis
- **Images**: OCR text extraction from receipts, invoices, documents
- **Batch Processing**: Handle multiple files simultaneously

### 🎭 Role-Based Intelligence
- **Pre-defined Roles**: CFO, Regional Sales Manager, Financial Analyst, Marketing Director, Operations Manager
- **Dynamic Filtering**: Insights automatically filtered by role requirements
- **Customizable Hierarchies**: Define your own organizational roles
- **Context-Aware**: Adapts metrics, granularity, and focus areas per role

### 📈 Advanced Analytics
- **Trend Detection**: Identify patterns in time-series data
- **Anomaly Detection**: Flag unusual patterns requiring attention
- **Correlation Analysis**: Discover relationships between variables
- **Comparative Analytics**: Benchmark across regions, periods, or categories
- **Statistical Significance**: Confidence scores for all insights

### 💬 Conversational AI Interface
- **Natural Language Queries**: Ask questions in plain English
- **Follow-up Questions**: Drill down into specific insights
- **Context Retention**: Maintains conversation history
- **LLM Integration**: Powered by Ollama (Mistral/Llama)

### 🔍 Explainable AI
- **Transparency**: Clear explanations for every insight
- **Data Provenance**: Track source data for each conclusion
- **Confidence Scores**: Quantified certainty levels
- **Recommendations**: Actionable suggestions with rationale

### 📊 Interactive Visualizations
- **Auto-generated Charts**: Role-appropriate visualizations
- **Multiple Chart Types**: Line, bar, scatter, heatmaps, treemaps
- **Interactive Dashboards**: Built with Plotly
- **Export Capabilities**: Download charts and reports

### 🔄 Continuous Learning
- **Feedback Collection**: Rate insights and provide comments
- **Adaptive Learning**: System improves based on user preferences
- **Performance Tracking**: Monitor accuracy and relevance metrics

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Interface (Streamlit)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Data Upload  │  │   Insights   │  │     Chat     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌────────▼────────┐
│   Module 1     │  │    Module 2     │  │    Module 3     │
│ Input Process  │──│  Role Context   │──│ Insight Engine  │
│  • Structured  │  │  • Role Maps    │  │  • Statistical  │
│  • Text (NLP)  │  │  • Requirements │  │  • Explainable  │
│  • Image (OCR) │  │  • Hierarchies  │  │  • Generation   │
└────────────────┘  └─────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌────────▼────────┐
│   Module 4     │  │    Module 5     │  │  Visualization  │
│ Conversation   │  │  Feedback &     │  │    Engine       │
│  • LLM (Ollama)│  │   Learning      │  │  • Charts       │
│  • RAG         │  │  • Adaptive     │  │  • Reports      │
│  • Context     │  │  • Analytics    │  │  • Export       │
└────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.10+** - Primary programming language
- **Streamlit** - Web application framework
- **FastAPI** - API framework (for future extensions)
- **Pandas/NumPy** - Data processing and analysis
- **Plotly** - Interactive visualizations

### NLP & Machine Learning
- **spaCy** - Named Entity Recognition
- **Transformers (Hugging Face)** - Sentiment analysis
- **sentence-transformers** - Text embeddings
- **scikit-learn** - Statistical analysis
- **scipy** - Scientific computing

### Document Processing
- **PyPDF2** - PDF text extraction
- **python-docx** - Word document processing
- **pytesseract** - Optical Character Recognition (OCR)
- **openpyxl** - Excel file handling

### LLM Integration
- **Ollama** - Local LLM inference
- **LangChain** - LLM orchestration and RAG
- **Mistral/Llama** - Open-source language models

### Data & Storage
- **SQLite** - Local database (future)
- **JSON** - Configuration and data exchange

---

## 📦 Installation

### Prerequisites

Before you begin, ensure you have:
- **Python 3.10 or higher** ([Download](https://www.python.org/downloads/))
- **pip** (Python package manager)
- **Tesseract OCR** (for image processing)
- **Ollama** (for conversational AI) - Optional

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd intelligent-report-system
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

### Step 4: Download NLP Models

```bash
# Download spaCy English model
python -m spacy download en_core_web_sm

# Download sentiment analysis model (happens automatically on first run)
```

### Step 5: Install Tesseract OCR

**Windows:**
1. Download installer: [Tesseract Windows](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install and note the installation path (e.g., `C:\Program Files\Tesseract-OCR\tesseract.exe`)
3. Update `.env` file with the path

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

### Step 6: Install Ollama (Optional - for Chat Feature)

**Linux/Mac:**
```bash
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull mistral
```

**Windows:**
Download from [ollama.com](https://ollama.com)

### Step 7: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

Example `.env`:
```bash
# LLM Settings
LLM_MODEL=mistral
LLM_BASE_URL=http://localhost:11434

# OCR Settings
TESSERACT_PATH=/usr/bin/tesseract  # Update for your system
OCR_LANGUAGE=eng

# NLP Settings
SPACY_MODEL=en_core_web_sm

# Logging
LOG_LEVEL=INFO
```

---

## 🚀 Quick Start

### Option 1: Use the Automated Script

```bash
# Make script executable (Linux/Mac)
chmod +x quickstart.sh

# Run quick start
./quickstart.sh
```

### Option 2: Manual Start

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Run the Streamlit app
streamlit run streamlit_app.py
```

The application will open in your default browser at `http://localhost:8501`

---

## 📘 Usage Guide

### 1️⃣ Initialize the System

1. Open the web interface
2. Navigate to **Home** page
3. Click **"Initialize System"** button
4. Wait for all modules to load (first time may take 1-2 minutes)

### 2️⃣ Select Your Role

In the sidebar, select your organizational role:
- **CFO** - Strategic, high-level financial insights
- **Regional Sales Manager** - Territory-specific sales metrics
- **Financial Analyst** - Detailed financial analysis
- **Marketing Director** - Campaign and market insights
- **Operations Manager** - Operational efficiency metrics

### 3️⃣ Upload Data

**Data Processing Page:**
1. Click **"Browse files"**
2. Select one or more files (CSV, Excel, PDF, images)
3. Click **"Process Data"**
4. Review processing results

**Supported formats:**
- Structured: `.csv`, `.xlsx`, `.xls`
- Documents: `.pdf`, `.docx`, `.txt`
- Images: `.jpg`, `.png`, `.bmp`, `.tiff`

### 4️⃣ Generate Insights

**Insights Page:**
1. Ensure data is processed
2. Click **"Generate Insights"**
3. View auto-generated insights for your role
4. Use filters to refine results:
   - Insight Type (Trend, Anomaly, Comparison, etc.)
   - Severity (Critical, High, Medium, Low)
   - Minimum Confidence

### 5️⃣ Explore with Chat

**Chat Interface:**
1. Navigate to **Chat** page
2. Type natural language questions:
   - "What are the key insights?"
   - "Why did sales decrease in Q3?"
   - "Show me regional performance"
   - "What should I focus on today?"
3. Ask follow-up questions for deeper analysis

### 6️⃣ Provide Feedback

For each insight:
1. Expand **"View Details"**
2. Rate the insight (1-5 stars)
3. Mark as relevant/not relevant
4. Submit feedback
5. System learns from your preferences

---

## 📁 Project Structure

```
intelligent-report-system/
├── src/
│   ├── modules/
│   │   ├── input_processing/           # Module 1: Data ingestion
│   │   │   ├── __init__.py
│   │   │   ├── models.py              # Data models (Pydantic)
│   │   │   ├── processor.py           # Main coordinator
│   │   │   ├── structured_processor.py # CSV, Excel handling
│   │   │   ├── text_processor.py      # PDF, DOCX, TXT + NLP
│   │   │   └── image_processor.py     # OCR processing
│   │   │
│   │   ├── role_context/              # Module 2: Role management
│   │   │   ├── __init__.py
│   │   │   ├── models.py              # Role definitions
│   │   │   ├── context_analyzer.py    # Role-context mapping
│   │   │   └── requirements.py        # Insight requirements
│   │   │
│   │   ├── insight_generation/        # Module 3: Analytics engine
│   │   │   ├── __init__.py
│   │   │   ├── models.py              # Insight models
│   │   │   ├── generator.py           # Main insight generator
│   │   │   ├── statistical_analyzer.py # Statistical methods
│   │   │   └── explainability.py      # XAI components
│   │   │
│   │   ├── conversational_interface/  # Module 4: Chat system
│   │   │   ├── __init__.py
│   │   │   ├── models.py              # Conversation models
│   │   │   ├── conversation_manager.py # Chat orchestration
│   │   │   ├── llm_integration.py     # Ollama integration
│   │   │   └── query_processor.py     # Query understanding
│   │   │
│   │   ├── feedback_learning/         # Module 5: Learning system
│   │   │   ├── __init__.py
│   │   │   ├── models.py              # Feedback models
│   │   │   ├── feedback_collector.py  # Feedback capture
│   │   │   └── learning_engine.py     # Adaptive algorithms
│   │   │
│   │   └── visualization/             # Visualization engine
│   │       ├── __init__.py
│   │       ├── chart_generator.py     # Chart creation
│   │       └── report_builder.py      # Report assembly
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py                # System configuration
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py                  # Logging setup
│       └── sample_data_generator.py   # Test data creation
│
├── data/
│   ├── raw/                           # Raw uploaded files
│   ├── processed/                     # Processed data
│   └── sample/                        # Sample/test data
│
├── logs/                              # Application logs
│
├── tests/
│   ├── test_module1.py                # Module 1 tests
│   ├── test_module2.py                # Module 2 tests
│   ├── test_module3.py                # Module 3 tests
│   ├── test_integration.py            # Integration tests
│   └── test_demo.py                   # Demo script
│
├── docs/                              # Additional documentation
│   ├── architecture.md
│   ├── api_reference.md
│   └── user_guide.md
│
├── streamlit_app.py                   # Main Streamlit application
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment template
├── .env                               # Your configuration (not in git)
├── .gitignore                         # Git ignore rules
├── setup.py                           # Package setup
├── quickstart.sh                      # Quick start script
└── README.md                          # This file
```

---

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# ============================================
# LLM Configuration (Ollama)
# ============================================
LLM_MODEL=mistral                    # Model name (mistral, llama2, etc.)
LLM_BASE_URL=http://localhost:11434 # Ollama server URL
LLM_TEMPERATURE=0.7                  # Response randomness (0.0-1.0)
LLM_MAX_TOKENS=2000                  # Max response length

# ============================================
# OCR Configuration (Tesseract)
# ============================================
TESSERACT_PATH=/usr/bin/tesseract   # Path to tesseract binary
OCR_LANGUAGE=eng                     # OCR language (eng, spa, fra, etc.)
OCR_CONFIDENCE_THRESHOLD=60          # Min confidence for text (0-100)

# ============================================
# NLP Configuration (spaCy)
# ============================================
SPACY_MODEL=en_core_web_sm          # spaCy model name
NER_CONFIDENCE_THRESHOLD=0.7        # Min confidence for entities

# ============================================
# Statistical Analysis
# ============================================
TREND_WINDOW=7                      # Days for trend analysis
ANOMALY_THRESHOLD=2.5               # Standard deviations for anomaly
CORRELATION_THRESHOLD=0.7           # Min correlation coefficient
STATISTICAL_SIGNIFICANCE=0.05       # P-value threshold

# ============================================
# Insight Generation
# ============================================
MIN_CONFIDENCE_SCORE=0.6            # Min confidence for insights
MAX_INSIGHTS_PER_ROLE=20            # Max insights to generate
ENABLE_EXPLANATIONS=true            # Generate explanations

# ============================================
# Logging
# ============================================
LOG_LEVEL=INFO                      # DEBUG, INFO, WARNING, ERROR
LOG_FILE_PATH=logs/                 # Log directory
LOG_ROTATION=daily                  # daily, weekly, monthly

# ============================================
# Performance
# ============================================
BATCH_SIZE=100                      # Rows per batch processing
MAX_FILE_SIZE_MB=100                # Max upload size
ENABLE_CACHING=true                 # Cache processed data
```

---

## 📚 Module Documentation

### Module 1: Multi-Modal Input Processing

**Purpose:** Ingest and standardize data from multiple sources

**Capabilities:**
- CSV/Excel parsing with schema detection
- PDF/DOCX text extraction
- Image OCR with confidence scoring
- NER and sentiment analysis
- Batch processing

**Example:**
```python
from src.modules.input_processing.processor import InputProcessor

processor = InputProcessor()
result = processor.process_file('sales_data.csv')
print(f"Processed {result.metadata.row_count} rows")
```

### Module 2: Role-Context Analyzer

**Purpose:** Map organizational roles to insight requirements

**Pre-defined Roles:**
- **CFO**: Strategic financial metrics, enterprise-wide trends
- **Regional Sales Manager**: Territory-specific sales, team performance
- **Financial Analyst**: Detailed financial analysis, variance reports
- **Marketing Director**: Campaign performance, market trends
- **Operations Manager**: Efficiency metrics, process improvements

**Example:**
```python
from src.modules.role_context.context_analyzer import RoleContextAnalyzer

analyzer = RoleContextAnalyzer()
context = analyzer.create_role_context('cfo')
print(f"Focus areas: {context.focus_areas}")
```

### Module 3: Insight Generation Engine

**Purpose:** Generate role-specific insights with explanations

**Insight Types:**
- **Trends**: Patterns over time
- **Anomalies**: Unusual values requiring attention
- **Comparisons**: Benchmarks across groups
- **Correlations**: Relationships between variables
- **Forecasts**: Predictions (coming soon)

**Example:**
```python
from src.modules.insight_generation.generator import InsightGenerator

generator = InsightGenerator()
insights = generator.generate_insights(
    data={'sales_df': df},
    role_id='regional_sales_manager'
)
print(f"Generated {len(insights.insights)} insights")
```

### Module 4: Conversational Interface

**Purpose:** Enable natural language interaction

**Features:**
- Question answering
- Follow-up context retention
- RAG (Retrieval-Augmented Generation)
- Multi-turn conversations

**Example:**
```python
from src.modules.conversational_interface.conversation_manager import ConversationManager

manager = ConversationManager(use_llm=True)
session = manager.create_session()
response = manager.process_message(session, "What are the key insights?")
print(response.response_text)
```

### Module 5: Feedback & Learning System

**Purpose:** Collect feedback and adapt system behavior

**Metrics Tracked:**
- Insight relevance ratings
- User interactions
- Feature usage
- Error patterns

**Example:**
```python
from src.modules.feedback_learning.feedback_collector import FeedbackCollector

collector = FeedbackCollector()
collector.record_insight_feedback(
    insight_id="ins_123",
    rating=5,
    is_relevant=True,
    role_id="cfo"
)
```

---

## 🔧 Recent Fixes (November 2025)

### Fixed Issues

#### ✅ Issue #1: Zero Insights Generated
**Problem:** Filtering logic was too strict, resulting in 0 insights displayed

**Solution:** 
- Implemented flexible type matching with synonyms
- Added role-specific overrides
- Lowered confidence threshold by 10%
- Added fallback to return top 3 insights if all filtered out

**Files Changed:**
- `src/modules/insight_generation/generator.py` - `_filter_for_role()` method

#### ✅ Issue #2: Deprecation Warning
**Problem:** `use_column_width` parameter deprecated in Streamlit

**Solution:**
- Replaced all `use_column_width=True` with `use_container_width=True`

**Files Changed:**
- `streamlit_app.py` - All st.image() calls

#### ✅ Issue #3: White Text on White Background
**Problem:** Insight cards had white text on white background

**Solution:**
- Added explicit color declarations in CSS
- Added `!important` flags to override conflicting styles
- Added dark mode support with media queries

**Files Changed:**
- `streamlit_app.py` - CSS styling in st.markdown()

### How to Apply Fixes

If you're using an older version, see the `QUICK_FIX_GUIDE.md` file for detailed instructions on applying these fixes.

---

## 🔍 Troubleshooting

### Common Issues

#### Issue: "spaCy model not found"
```bash
# Solution:
python -m spacy download en_core_web_sm
```

#### Issue: "Tesseract not found"
```bash
# Verify installation:
tesseract --version

# If not installed, install per OS instructions above
# Then update TESSERACT_PATH in .env
```

#### Issue: "Out of memory during processing"
```bash
# Reduce batch size in .env:
BATCH_SIZE=50

# Or process fewer files at once
```

#### Issue: "Ollama connection failed"
```bash
# Check Ollama is running:
ollama list

# Start Ollama if needed:
ollama serve

# Verify URL in .env matches:
LLM_BASE_URL=http://localhost:11434
```

#### Issue: "No insights generated"
```bash
# Check logs:
tail -f logs/app_*.log

# Verify data was processed:
# Go to Data Processing page and confirm success

# Check role requirements match data:
# CFO needs aggregate data, Regional Manager needs region column
```

#### Issue: "Streamlit page blank/white"
```bash
# Clear browser cache or use incognito mode
# Or clear Streamlit cache:
streamlit cache clear

# Restart Streamlit:
Ctrl+C (to stop)
streamlit run streamlit_app.py
```

### Debug Mode

Enable debug logging:
```bash
# In .env:
LOG_LEVEL=DEBUG

# Or temporarily:
export LOG_LEVEL=DEBUG
streamlit run streamlit_app.py
```

View logs:
```bash
# Real-time monitoring:
tail -f logs/app_*.log

# View errors only:
tail -f logs/errors_*.log
```

---

## 🧪 Testing

### Run All Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest --cov=src tests/
```

### Test Individual Modules

```bash
# Test Module 1 (Input Processing)
python tests/test_module1.py

# Test Module 2 (Role Context)
python tests/test_module2.py

# Test Module 3 (Insights)
python tests/test_module3.py

# Integration test
python tests/test_integration.py

# Full demo
python tests/test_demo.py
```

### Sample Output

```
================================================================================
  INTELLIGENT REPORT SYSTEM - COMPLETE DEMO
================================================================================

✅ System Initialization: WORKING
✅ Multi-Modal Input Processing: WORKING
✅ Role Context Analysis: WORKING
✅ Insight Generation: WORKING
✅ Conversational Interface: WORKING
✅ Feedback Collection: WORKING
✅ Learning Engine: WORKING

Generated Insights:
  CFO: 8 insights (avg confidence: 85%)
  Regional Manager: 12 insights (avg confidence: 88%)
  Financial Analyst: 10 insights (avg confidence: 90%)

================================================================================
All systems operational! ✨
================================================================================
```

---

## 🚀 Deployment

### Local Deployment

```bash
# Run on all network interfaces:
streamlit run streamlit_app.py --server.address=0.0.0.0

# Custom port:
streamlit run streamlit_app.py --server.port=8080
```

### Production Deployment Options

#### Option 1: Streamlit Cloud (Free)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy!

#### Option 2: Docker
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

```bash
docker build -t intelligent-reports .
docker run -p 8501:8501 intelligent-reports
```

#### Option 3: Cloud Platforms
- **AWS**: EC2, ECS, or Elastic Beanstalk
- **Google Cloud**: Cloud Run or App Engine  
- **Azure**: App Service or Container Instances
- **Heroku**: With Procfile

### Background Service (Linux)

```bash
# Using tmux:
tmux new -s reports
streamlit run streamlit_app.py
# Detach: Ctrl+B, then D

# Using systemd:
sudo nano /etc/systemd/system/reports.service
# [Service]
# ExecStart=/path/to/venv/bin/streamlit run streamlit_app.py

sudo systemctl start reports
sudo systemctl enable reports
```

---

## 👥 Contributing

This is an academic project. For questions or suggestions:

1. **Issues**: Report bugs or request features
2. **Pull Requests**: Contributions welcome
3. **Documentation**: Help improve docs
4. **Testing**: Add test cases

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run pre-commit hooks
pre-commit install

# Run linters
flake8 src/
black src/
mypy src/
```

---

## 🎓 Academic Context

### Master's Thesis Project

**Title:** Context-Aware Automated Report Generation System with Role-Based Data Visualization and Insights

**Institution:** [Your University]  
**Department:** [Computer Science / Data Science]  
**Year:** 2024-2025

### Research Questions

1. How can NLP and data analytics be combined to automatically identify role-relevant insights?
2. What framework effectively maps organizational roles to data granularity and visualization types?
3. How can context-aware algorithms determine actionable insights for specific decision-making levels?
4. What design principles ensure reports maintain analytical rigor while remaining accessible?

### Key Contributions

- **Multi-Modal Processing Framework**: Unified handling of structured, text, and image data
- **Role-Based Insight Ontology**: Formal mapping of roles to insight requirements
- **Explainable Analytics**: Transparent AI with data provenance and confidence scoring
- **Adaptive Learning System**: Feedback-driven improvement of relevance and accuracy

### Publications & Presentations

- [Add your publications]
- [Conference presentations]
- [Workshop papers]

---

## 📄 License

[Specify your license - MIT, Apache 2.0, etc.]

---

## 🙏 Acknowledgments

- **spaCy** - Industrial-strength NLP
- **Hugging Face** - Transformer models and ecosystem
- **Tesseract OCR** - Google's text extraction engine
- **Ollama** - Local LLM inference
- **Streamlit** - Beautiful data apps framework
- **Plotly** - Interactive visualizations
- **Open-source community** - Countless libraries and tools

---

## 📞 Contact & Support

- **Email**: [your.email@university.edu]
- **GitHub**: [your-github-username]
- **LinkedIn**: [your-linkedin]
- **Project Website**: [if applicable]

---

## 📊 Project Status

| Module | Status | Completion | Last Updated |
|--------|--------|------------|--------------|
| Module 1: Input Processing | ✅ Complete | 100% | Oct 2024 |
| Module 2: Role Context | ✅ Complete | 100% | Oct 2024 |
| Module 3: Insight Generation | ✅ Complete | 100% | Nov 2024 |
| Module 4: Conversational AI | ✅ Complete | 100% | Nov 2024 |
| Module 5: Learning System | ✅ Complete | 100% | Nov 2024 |
| Streamlit Interface | ✅ Complete | 100% | Nov 2024 |
| Documentation | ✅ Complete | 100% | Nov 2024 |
| Testing Suite | ✅ Complete | 95% | Nov 2024 |
| Deployment Ready | ✅ Yes | 100% | Nov 2024 |

**Overall Project Status:** ✅ **Production Ready**

---

## 🗓️ Changelog

### Version 1.0.0 (November 2024)
- ✅ All 5 modules complete and integrated
- ✅ Streamlit web interface launched
- ✅ Fixed filtering logic (zero insights bug)
- ✅ Fixed UI styling issues
- ✅ Comprehensive documentation
- ✅ Complete test suite

### Version 0.5.0 (October 2024)
- ✅ Modules 1-3 implemented
- ✅ Basic insight generation working
- ✅ Initial role definitions

### Version 0.1.0 (September 2024)
- ✅ Project structure established
- ✅ Module 1 prototype complete

---

## 📈 Future Roadmap

### Planned Features

- [ ] **API Layer**: RESTful API for programmatic access
- [ ] **Database Integration**: PostgreSQL for scalable storage
- [ ] **Advanced Forecasting**: Time-series predictions
- [ ] **Custom Role Builder**: UI for defining new roles
- [ ] **Report Templates**: Pre-designed report formats
- [ ] **Email Integration**: Scheduled report delivery
- [ ] **Mobile App**: iOS/Android companion apps
- [ ] **Multi-language Support**: i18n for global use
- [ ] **Enhanced Visualizations**: 3D charts, network graphs
- [ ] **Collaborative Features**: Multi-user annotations

---

**Built with ❤️ for data-driven decision making**

*Last Updated: November 3, 2025*