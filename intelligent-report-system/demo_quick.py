"""
QUICK DEMO - All Modules in 2 Minutes
Fast demonstration without user interaction
Run: python demo_quick.py
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

from src.modules.input_processing.processor import InputProcessor
from src.modules.role_context.context_analyzer import RoleContextAnalyzer
from src.modules.insight_generation.generator import InsightGenerator
from src.modules.conversational_interface.manager import ConversationManager
from src.modules.feedback_learning.collector import FeedbackCollector
from src.modules.feedback_learning.learning_engine import LearningEngine
from src.utils.sample_data_generator import SampleDataGenerator

def quick_demo():
    print("\n" + "="*70)
    print("  QUICK SYSTEM DEMO - All 5 Modules")
    print("="*70 + "\n")
    
    # Initialize
    print("[1/6] Initializing system...")
    input_processor = InputProcessor()
    context_analyzer = RoleContextAnalyzer()
    insight_generator = InsightGenerator()
    conversation_manager = ConversationManager(use_llm=True)
    feedback_collector = FeedbackCollector()
    learning_engine = LearningEngine(feedback_collector)
    generator = SampleDataGenerator()
    print("✓ All modules initialized\n")
    
    # Process data
    print("[2/6] Processing data...")
    sales_file = generator.generate_sales_data(num_rows=300)
    sales_data = input_processor.process_file(sales_file)
    print(f"✓ Processed {sales_data.metadata.row_count} rows\n")
    
    # Generate insights
    print("[3/6] Generating insights...")
    insights = insight_generator.generate_insights(sales_data)
    print(f"✓ Generated {insights.total_count} insights")
    print(f"  Top insight: {insights.insights[0].title}\n")
    
    # Role-based
    print("[4/6] Role-based filtering...")
    role_context = context_analyzer.create_role_context("cfo")
    kpis = context_analyzer.get_relevant_kpis("cfo")
    print(f"✓ CFO view: {', '.join(kpis[:3])}\n")
    
    # Conversation
    print("[5/6] Conversational interface...")
    session_id = conversation_manager.create_session()
    response = conversation_manager.process_message(
        session_id, 
        "What are the key insights?",
        insights
    )
    print(f"✓ Query processed: {response.intent.value}")
    print(f"  Response: {response.response_text[:100]}...\n")
    
    # Feedback
    print("[6/6] Feedback & learning...")
    feedback_collector.record_insight_feedback(
        insight_id=insights.insights[0].insight_id,
        rating=5,
        role_id="cfo"
    )
    learning_engine.adapt_system()
    print(f"✓ Feedback collected and system adapted\n")
    
    # Summary
    print("="*70)
    print("  DEMO COMPLETE - ALL MODULES WORKING!")
    print("="*70)
    print(f"\n✓ Data processed: {sales_data.metadata.row_count} rows")
    print(f"✓ Insights generated: {insights.total_count}")
    print(f"✓ Roles configured: 5")
    print(f"✓ LLM enabled: {conversation_manager.use_llm}")
    print(f"✓ Feedback collected: Yes")
    print(f"✓ System learning: Active\n")

if __name__ == "__main__":
    quick_demo()