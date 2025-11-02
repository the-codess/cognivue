"""
Streamlit Web Interface for Intelligent Report Generation System
Run: streamlit run streamlit_app.py
"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Add project root to path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

from src.modules.input_processing.processor import InputProcessor
from src.modules.role_context.context_analyzer import RoleContextAnalyzer
from src.modules.insight_generation.generator import InsightGenerator
from src.modules.conversational_interface.manager import ConversationManager
from src.modules.feedback_learning.collector import FeedbackCollector
from src.modules.feedback_learning.learning_engine import LearningEngine
from src.utils.sample_data_generator import SampleDataGenerator

# Page config
st.set_page_config(
    page_title="Intelligent Report System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# # Custom CSS
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 2.5rem;
#         font-weight: bold;
#         color: #1f77b4;
#         text-align: center;
#         margin-bottom: 2rem;
#     }
#     .metric-card {
#         background-color: #f0f2f6;
#         padding: 1rem;
#         border-radius: 0.5rem;
#         border-left: 4px solid #1f77b4;
#     }
#     .insight-card {
#         background-color: #ffffff;
#         padding: 1.5rem;
#         border-radius: 0.5rem;
#         border: 1px solid #e0e0e0;
#         margin-bottom: 1rem;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
#     .stButton>button {
#         width: 100%;
#     }
# </style>
# """, unsafe_allow_html=True)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: rgba(240, 242, 246, 0.9);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #262730 !important;  /* Force dark text */
    }
    .insight-card h3 {
        color: #1a1a1a !important;
        margin-bottom: 0.5rem;
        font-size: 1.3rem;
    }
    .insight-card p {
        color: #3d3d3d !important;
        line-height: 1.6;
    }
    .insight-card strong {
        color: #1a1a1a !important;
        font-weight: 600;
    }
    .stButton>button {
        width: 100%;
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .insight-card {
            background-color: rgba(38, 39, 48, 0.95);
            border-color: #464646;
            color: #e0e0e0 !important;
        }
        .insight-card h3 {
            color: #ffffff !important;
        }
        .insight-card p {
            color: #d0d0d0 !important;
        }
        .insight-card strong {
            color: #ffffff !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.input_processor = None
    st.session_state.context_analyzer = None
    st.session_state.insight_generator = None
    st.session_state.conversation_manager = None
    st.session_state.feedback_collector = None
    st.session_state.learning_engine = None
    st.session_state.insights = None
    st.session_state.processed_data = None
    st.session_state.chat_history = []
    st.session_state.session_id = None

def initialize_system():
    """Initialize all system components"""
    with st.spinner("🚀 Initializing system components..."):
        st.session_state.input_processor = InputProcessor()
        st.session_state.context_analyzer = RoleContextAnalyzer()
        st.session_state.insight_generator = InsightGenerator()
        st.session_state.conversation_manager = ConversationManager(use_llm=True)
        st.session_state.feedback_collector = FeedbackCollector()
        st.session_state.learning_engine = LearningEngine(st.session_state.feedback_collector)
        st.session_state.initialized = True
        st.session_state.session_id = st.session_state.conversation_manager.create_session()
    st.success("✅ System initialized successfully!")

def create_metric_card(label, value, delta=None):
    """Create a styled metric display"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.metric(label, value, delta)

def display_insight_card(insight, index):
    """Display insight in a card format"""
    severity_colors = {
        "critical": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢",
        "info": "🔵"
    }
    
    severity_icon = severity_colors.get(insight.severity.value, "⚪")
    
    with st.container():
        st.markdown(f"""
        <div class="insight-card">
            <h3>{severity_icon} {insight.title}</h3>
            <p><strong>Type:</strong> {insight.insight_type.value.title()} | 
               <strong>Confidence:</strong> {insight.confidence_score:.1%} | 
               <strong>Impact:</strong> {insight.impact_score:.1%}</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📊 View Details"):
            st.write("**Description:**", insight.description)
            st.write("**Analysis:**", insight.narrative)
            
            if insight.explanations:
                st.write("**Explanations:**")
                for exp in insight.explanations:
                    st.info(f"• {exp.content} (Confidence: {exp.confidence:.1%})")
            
            if insight.recommendations:
                st.write("**Recommendations:**")
                for rec in insight.recommendations:
                    st.success(f"• {rec}")
            
            if insight.key_metrics:
                st.write("**Key Metrics:**")
                st.json(insight.key_metrics)
            
            # Feedback
            col1, col2, col3 = st.columns(3)
            with col1:
                rating = st.slider(
                    "Rate this insight", 
                    1, 5, 3, 
                    key=f"rating_{insight.insight_id}"
                )
            with col2:
                relevant = st.checkbox("Relevant", key=f"rel_{insight.insight_id}")
            with col3:
                if st.button("Submit Feedback", key=f"fb_{insight.insight_id}"):
                    st.session_state.feedback_collector.record_insight_feedback(
                        insight_id=insight.insight_id,
                        rating=rating,
                        is_relevant=relevant,
                        role_id=st.session_state.selected_role
                    )
                    st.success("Feedback recorded!")

# Sidebar
with st.sidebar:
    # st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=Intelligent+Reports", use_column_width=True)
    # st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=Intelligent+Reports", use_container_width=True)

    st.markdown("### 🎯 Navigation")
    page = st.radio(
        "Select Module",
        ["🏠 Home", "📊 Data Processing", "🔍 Insights", "💬 Chat", "📈 Learning", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("### 👤 User Profile")
    role_options = {
        "cfo": "Chief Financial Officer",
        "regional_sales_manager": "Regional Sales Manager",
        "financial_analyst": "Financial Analyst",
        "marketing_director": "Marketing Director",
        "operations_manager": "Operations Manager"
    }
    
    st.session_state.selected_role = st.selectbox(
        "Select Your Role",
        options=list(role_options.keys()),
        format_func=lambda x: role_options[x],
        key="role_selector"
    )
    
    st.markdown("---")
    
    if not st.session_state.initialized:
        if st.button("🚀 Initialize System", use_container_width=True):
            initialize_system()
    else:
        st.success("✅ System Online")
        
        if st.session_state.conversation_manager.use_llm:
            st.info(f"🤖 LLM: {st.session_state.conversation_manager.llm_handler.model_name}")
        else:
            st.warning("🔄 Pattern Matching Mode")

# Main content
if page == "🏠 Home":
    st.markdown('<p class="main-header">📊 Cognivue </p>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Welcome to the Context-Aware Report Generation System
    
    This system combines **multi-modal analytics**, **explainable AI**, and **conversational interfaces** 
    to deliver personalized insights based on your organizational role.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 📥 Module 1
        **Multi-Modal Input Processing**
        - CSV, Excel, PDF, DOCX
        - Entity extraction
        - Sentiment analysis
        - OCR capabilities
        """)
    
    with col2:
        st.markdown("""
        #### 🎯 Module 2
        **Role-Context Analyzer**
        - 5 organizational roles
        - Role-based filtering
        - KPI mapping
        - Access control
        """)
    
    with col3:
        st.markdown("""
        #### 🔍 Module 3
        **Insight Generation**
        - Trend detection
        - Anomaly detection
        - Correlations
        - Explainable AI
        """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 💬 Module 4
        **Conversational Interface**
        - Natural language queries
        - LLM-powered responses
        - Multi-turn conversations
        - Context awareness
        """)
    
    with col2:
        st.markdown("""
        #### 📈 Module 5
        **Feedback & Learning**
        - User feedback collection
        - Adaptive learning
        - Continuous improvement
        - Performance metrics
        """)
    
    st.markdown("---")
    
    if st.session_state.initialized:
        st.success("✅ System is ready! Navigate using the sidebar to explore different modules.")
    else:
        st.warning("⚠️ Please initialize the system using the button in the sidebar.")

elif page == "📊 Data Processing":
    st.header("📊 Multi-Modal Data Processing")
    
    if not st.session_state.initialized:
        st.error("Please initialize the system first!")
        st.stop()
    
    tab1, tab2, tab3 = st.tabs(["📁 Upload Data", "🎲 Generate Sample", "📋 View Data"])
    
    with tab1:
        st.subheader("Upload Your Data")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'xlsx', 'pdf', 'docx', 'txt', 'png', 'jpg'],
            help="Supported formats: CSV, Excel, PDF, Word, Text, Images"
        )
        
        if uploaded_file:
            with st.spinner("Processing file..."):
                # Save temp file
                temp_path = f"data/temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Process
                result = st.session_state.input_processor.process_file(temp_path)
                st.session_state.processed_data = result
                
                st.success(f"✅ Processed: {uploaded_file.name}")
                
                # Display info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Modality", result.modality.value.title())
                with col2:
                    st.metric("Source Type", result.source_type.value.upper())
                with col3:
                    st.metric("Status", result.status.value.title())
    
    with tab2:
        st.subheader("Generate Sample Data")
        
        data_type = st.selectbox(
            "Select data type",
            ["Sales Data (CSV)", "Financial Report (Text)", "Customer Feedback (Text)", "Invoice (Image)"]
        )
        
        if data_type == "Sales Data (CSV)":
            num_rows = st.slider("Number of rows", 100, 1000, 500)
        
        if st.button("🎲 Generate Data"):
            generator = SampleDataGenerator()
            
            with st.spinner("Generating..."):
                if data_type == "Sales Data (CSV)":
                    file_path = generator.generate_sales_data(num_rows)
                elif data_type == "Financial Report (Text)":
                    file_path = generator.generate_financial_report()
                elif data_type == "Customer Feedback (Text)":
                    file_path = generator.generate_customer_feedback()
                else:
                    file_path = generator.generate_sample_invoice_image()
                
                # Process
                result = st.session_state.input_processor.process_file(file_path)
                st.session_state.processed_data = result
                
                st.success(f"✅ Generated and processed!")
                
                # Show preview
                if hasattr(result.metadata, 'row_count'):
                    st.metric("Rows", result.metadata.row_count)
                    st.metric("Columns", result.metadata.column_count)
                elif hasattr(result.metadata, 'word_count'):
                    st.metric("Words", result.metadata.word_count)
                    st.metric("Entities", len(result.metadata.entities))
    
    with tab3:
        if st.session_state.processed_data:
            st.subheader("Processed Data View")
            
            data = st.session_state.processed_data
            
            if data.modality.value == "structured":
                df = pd.DataFrame(data.processed_content['data'])
                st.dataframe(df, use_container_width=True)
                
                # Summary stats
                st.subheader("Summary Statistics")
                if data.metadata.summary_stats:
                    for col, stats in list(data.metadata.summary_stats.items())[:3]:
                        with st.expander(f"📊 {col}"):
                            col1, col2, col3, col4 = st.columns(4)
                            col1.metric("Mean", f"{stats['mean']:.2f}" if stats['mean'] else "N/A")
                            col2.metric("Median", f"{stats['median']:.2f}" if stats['median'] else "N/A")
                            col3.metric("Min", f"{stats['min']:.2f}" if stats['min'] else "N/A")
                            col4.metric("Max", f"{stats['max']:.2f}" if stats['max'] else "N/A")
            
            elif data.modality.value == "text":
                st.text_area("Content Preview", data.processed_content[:500] + "...", height=200)
                
                if data.metadata:
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Words", data.metadata.word_count)
                    col2.metric("Sentences", data.metadata.sentence_count)
                    col3.metric("Entities", len(data.metadata.entities))
                    
                    if data.metadata.sentiment:
                        st.info(f"😊 Sentiment: {data.metadata.sentiment.label.title()} ({data.metadata.sentiment.score:.1%})")
        else:
            st.info("No data processed yet. Upload or generate data first.")

elif page == "🔍 Insights":
    st.header("🔍 Intelligent Insights")
    
    if not st.session_state.initialized:
        st.error("Please initialize the system first!")
        st.stop()
    
    if not st.session_state.processed_data:
        st.warning("Please process some data first in the Data Processing section!")
        st.stop()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Generate Insights")
    
    with col2:
        if st.button("🔮 Generate Insights", use_container_width=True):
            with st.spinner("Analyzing data..."):
                role_context = st.session_state.context_analyzer.create_role_context(
                    st.session_state.selected_role
                )
                insight_req = st.session_state.context_analyzer.get_insight_requirements(
                    st.session_state.selected_role
                )
                
                insights = st.session_state.insight_generator.generate_insights(
                    st.session_state.processed_data,
                    role_context,
                    insight_req
                )
                
                st.session_state.insights = insights
                st.success(f"✅ Generated {insights.total_count} insights!")
    
    if st.session_state.insights:
        insights = st.session_state.insights
        
        # Metrics
        st.markdown("### 📊 Overview")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Insights", insights.total_count)
        col2.metric("Avg Confidence", f"{insights.avg_confidence:.1%}")
        col3.metric("Critical", insights.critical_insights, delta_color="inverse")
        col4.metric("High Priority", insights.high_priority_insights)
        
        # Filters
        st.markdown("### 🎛️ Filters")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_type = st.multiselect(
                "Insight Type",
                options=list(set([i.insight_type.value for i in insights.insights])),
                default=list(set([i.insight_type.value for i in insights.insights]))
            )
        
        with col2:
            filter_severity = st.multiselect(
                "Severity",
                options=list(set([i.severity.value for i in insights.insights])),
                default=list(set([i.severity.value for i in insights.insights]))
            )
        
        with col3:
            min_confidence = st.slider("Min Confidence", 0.0, 1.0, 0.0, 0.1)
        
        # Filter insights
        filtered_insights = [
            i for i in insights.insights
            if i.insight_type.value in filter_type
            and i.severity.value in filter_severity
            and i.confidence_score >= min_confidence
        ]
        
        st.markdown(f"### 💡 Insights ({len(filtered_insights)} shown)")
        
        # Display insights
        for idx, insight in enumerate(filtered_insights, 1):
            display_insight_card(insight, idx)
    else:
        st.info("Click 'Generate Insights' to analyze your data!")

elif page == "💬 Chat":
    st.header("💬 Conversational Interface")
    
    if not st.session_state.initialized:
        st.error("Please initialize the system first!")
        st.stop()
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.chat_message("user").write(message['content'])
            else:
                st.chat_message("assistant").write(message['content'])
    
    # Chat input
    if prompt := st.chat_input("Ask me about your data..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.spinner("Thinking..."):
            response = st.session_state.conversation_manager.process_message(
                st.session_state.session_id,
                prompt,
                st.session_state.insights
            )
        
        # Add assistant response
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response.response_text
        })
        
        # Rerun to display new messages
        st.rerun()
    
    # Suggested questions
    if st.session_state.insights:
        st.markdown("### 💡 Suggested Questions")
        suggestions = [
            "What are the key insights?",
            "Why is this happening?",
            "What should I do about this?",
            "Show me the trends",
            "Are there any anomalies?"
        ]
        
        cols = st.columns(len(suggestions))
        for idx, suggestion in enumerate(suggestions):
            if cols[idx].button(suggestion, key=f"sugg_{idx}"):
                # Trigger chat with suggestion
                st.session_state.chat_history.append({"role": "user", "content": suggestion})
                
                with st.spinner("Thinking..."):
                    response = st.session_state.conversation_manager.process_message(
                        st.session_state.session_id,
                        suggestion,
                        st.session_state.insights
                    )
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response.response_text
                })
                
                st.rerun()

elif page == "📈 Learning":
    st.header("📈 Feedback & Learning")
    
    if not st.session_state.initialized:
        st.error("Please initialize the system first!")
        st.stop()
    
    tab1, tab2, tab3 = st.tabs(["📊 Metrics", "💭 Feedback", "🎯 Adaptation"])
    
    with tab1:
        st.subheader("Learning Metrics")
        
        if st.button("📊 Compute Metrics"):
            metrics = st.session_state.learning_engine.compute_learning_metrics()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("User Satisfaction", f"{metrics.user_satisfaction_score:.1%}")
            col2.metric("Positive Feedback", f"{metrics.positive_feedback_rate:.1%}")
            col3.metric("Improvement Rate", f"{metrics.improvement_rate:.1%}")
            
            col1, col2 = st.columns(2)
            col1.metric("Model Accuracy", f"{metrics.model_accuracy:.1%}")
            col2.metric("Total Feedback", metrics.total_feedback_count)
    
    with tab2:
        st.subheader("Feedback Summary")
        
        summary = st.session_state.feedback_collector.get_feedback_summary(days=30)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Feedback", summary.total_feedback)
        col2.metric("Average Rating", f"{summary.avg_rating:.2f}/5")
        col3.metric("Positive Rate", f"{summary.positive_rate:.1%}")
        col4.metric("Negative Rate", f"{summary.negative_rate:.1%}")
        
        # Feedback over time (placeholder chart)
        if summary.total_feedback > 0:
            st.line_chart([summary.avg_rating] * 7)
    
    with tab3:
        st.subheader("System Adaptation")
        
        if st.button("🔄 Adapt System"):
            with st.spinner("Learning from feedback..."):
                st.session_state.learning_engine.adapt_system()
                st.success("✅ System adapted!")
            
            st.info(f"✓ Updated weights for {len(st.session_state.learning_engine.insight_weights)} insights")
            st.info(f"✓ Learned preferences for {len(st.session_state.learning_engine.role_preferences)} roles")
        
        # Show adaptations
        if st.session_state.learning_engine.adaptation_history:
            st.subheader("Recent Adaptations")
            for action in st.session_state.learning_engine.adaptation_history[-5:]:
                st.success(f"✓ {action.action_type}: {action.expected_impact}")

else:  # Settings
    st.header("⚙️ System Settings")
    
    st.subheader("Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Enable LLM", value=True, disabled=True)
        st.selectbox("LLM Model", ["mistral", "llama2", "phi"])
        st.slider("LLM Temperature", 0.0, 1.0, 0.7)
    
    with col2:
        st.checkbox("Auto-generate insights", value=True)
        st.number_input("Max insights per report", 1, 50, 10)
        st.slider("Min confidence threshold", 0.0, 1.0, 0.7)
    
    st.markdown("---")
    
    st.subheader("System Information")
    
    if st.session_state.initialized:
        info = {
            "Status": "✅ Online",
            "Modules Loaded": "5/5",
            "LLM Available": "Yes" if st.session_state.conversation_manager.use_llm else "No",
            "Active Role": role_options.get(st.session_state.selected_role, "Unknown"),
            "Session ID": st.session_state.session_id[:16] + "..." if st.session_state.session_id else "N/A"
        }
        
        for key, value in info.items():
            st.text(f"{key}: {value}")
    else:
        st.warning("System not initialized")
    
    st.markdown("---")
    
    if st.button("🔄 Reset System"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Cognivue v1.0 | Built by the_codess </p>
</div>
""", unsafe_allow_html=True)