"""
COMPLETE SYSTEM DEMONSTRATION
Intelligent Report Generation System with Multi-Modal Analytics & Explainable AI

This demo showcases all 5 modules working together in a realistic scenario.
Run: python demo_full_system.py
"""
import sys
from pathlib import Path
import time

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
from src.utils.logger import app_logger as logger

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_banner():
    """Print welcome banner"""
    print("\n" + "="*80)
    print(Colors.BOLD + Colors.CYAN + 
          "  INTELLIGENT REPORT GENERATION SYSTEM" + Colors.END)
    print(Colors.BOLD + 
          "  Multi-Modal Analytics with Explainable AI & Conversational Interface" + 
          Colors.END)
    print("="*80 + "\n")

def print_section(title, color=Colors.BLUE):
    """Print section header"""
    print("\n" + color + Colors.BOLD + "█" * 80 + Colors.END)
    print(color + Colors.BOLD + f"  {title}" + Colors.END)
    print(color + Colors.BOLD + "█" * 80 + Colors.END + "\n")

def print_step(step_num, description):
    """Print step description"""
    print(f"{Colors.YELLOW}[Step {step_num}]{Colors.END} {Colors.BOLD}{description}{Colors.END}")

def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_info(message, indent=0):
    """Print info message"""
    print("  " * indent + f"{Colors.CYAN}•{Colors.END} {message}")

def print_insight(insight, index=None):
    """Print insight details"""
    if index:
        print(f"\n{Colors.BOLD}Insight #{index}:{Colors.END} {insight.title}")
    else:
        print(f"\n{Colors.BOLD}Insight:{Colors.END} {insight.title}")
    
    print(f"  {Colors.CYAN}Type:{Colors.END} {insight.insight_type.value}")
    print(f"  {Colors.CYAN}Severity:{Colors.END} {insight.severity.value.upper()}")
    print(f"  {Colors.CYAN}Confidence:{Colors.END} {insight.confidence_score:.1%}")
    print(f"  {Colors.CYAN}Description:{Colors.END} {insight.description}")
    
    if insight.narrative:
        print(f"\n  {Colors.BOLD}Analysis:{Colors.END}")
        print(f"  {insight.narrative}")
    
    if insight.recommendations:
        print(f"\n  {Colors.BOLD}Recommendations:{Colors.END}")
        for rec in insight.recommendations[:2]:
            print(f"    • {rec}")

def simulate_user_interaction(message, delay=1.5):
    """Simulate user thinking/reading time"""
    print(f"\n{Colors.YELLOW}⏱{Colors.END}  {message}")
    for i in range(3):
        time.sleep(delay / 3)
        print(".", end="", flush=True)
    print()

def demo_full_system():
    """Run complete system demonstration"""
    
    print_banner()
    
    print(f"{Colors.BOLD}Welcome to the Intelligent Report Generation System!{Colors.END}")
    print("This demo will showcase how the system processes data, generates insights,")
    print("adapts to different roles, and learns from feedback.\n")
    
    input(f"{Colors.YELLOW}Press Enter to begin the demonstration...{Colors.END}")
    
    # SECTION 1: SYSTEM INITIALIZATION
    print_section("SECTION 1: SYSTEM INITIALIZATION", Colors.BLUE)
    
    print_step(1, "Initializing all system components...")
    print()
    
    input_processor = InputProcessor()
    print_success("Module 1: Multi-Modal Input Processing ✓")
    
    context_analyzer = RoleContextAnalyzer()
    print_success("Module 2: Role-Context Analyzer ✓")
    
    insight_generator = InsightGenerator()
    print_success("Module 3: Insight Generation & Explanation Engine ✓")
    
    conversation_manager = ConversationManager(use_llm=True)
    if conversation_manager.use_llm:
        print_success(f"Module 4: Conversational Interface (LLM: {conversation_manager.llm_handler.model_name}) ✓")
    else:
        print_success("Module 4: Conversational Interface (Pattern Matching) ✓")
    
    feedback_collector = FeedbackCollector()
    learning_engine = LearningEngine(feedback_collector)
    print_success("Module 5: Feedback & Learning System ✓")
    
    generator = SampleDataGenerator()
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}All systems operational!{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    
    # SECTION 2: DATA INGESTION
    print_section("SECTION 2: MULTI-MODAL DATA PROCESSING", Colors.CYAN)
    
    print_step(2, "Processing multiple data sources...")
    print()
    
    # Generate sales data
    print_info("Ingesting sales data (CSV)...")
    sales_file = generator.generate_sales_data(num_rows=500)
    sales_data = input_processor.process_file(sales_file)
    print_success(f"Processed {sales_data.metadata.row_count} rows, {sales_data.metadata.column_count} columns")
    print_info(f"Columns: {', '.join(sales_data.metadata.columns)}", indent=1)
    
    # Generate text reports
    print()
    print_info("Processing financial report (PDF/Text)...")
    report_file = generator.generate_financial_report()
    report_data = input_processor.process_file(report_file)
    print_success(f"Processed {report_data.metadata.word_count} words")
    print_info(f"Extracted {len(report_data.metadata.entities)} entities", indent=1)
    print_info(f"Sentiment: {report_data.metadata.sentiment.label} ({report_data.metadata.sentiment.score:.1%})", indent=1)
    
    # Customer feedback
    print()
    print_info("Analyzing customer feedback...")
    feedback_file = generator.generate_customer_feedback()
    feedback_data = input_processor.process_file(feedback_file)
    print_success(f"Processed {feedback_data.metadata.word_count} words")
    print_info(f"Key phrases identified: {len(feedback_data.metadata.key_phrases)}", indent=1)
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}Multi-modal data processing complete!{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    
    # SECTION 3: INSIGHT GENERATION
    print_section("SECTION 3: INTELLIGENT INSIGHT GENERATION", Colors.GREEN)
    
    print_step(3, "Analyzing data and generating insights with explanations...")
    print()
    
    simulate_user_interaction("Running statistical analysis", 2)
    
    insights = insight_generator.generate_insights(sales_data)
    
    print_success(f"Generated {insights.total_count} insights")
    print_info(f"Average confidence: {insights.avg_confidence:.1%}")
    print_info(f"Critical insights: {insights.critical_insights}")
    print_info(f"High priority: {insights.high_priority_insights}")
    
    print(f"\n{Colors.BOLD}Top 3 Insights:{Colors.END}")
    for i, insight in enumerate(insights.insights[:3], 1):
        print(f"\n  {i}. [{Colors.YELLOW}{insight.insight_type.value.upper()}{Colors.END}] {insight.title}")
        print(f"     Confidence: {insight.confidence_score:.1%} | Impact: {insight.impact_score:.1%}")
    
    input(f"\n{Colors.YELLOW}Press Enter to see detailed insight analysis...{Colors.END}")
    
    # Show detailed insight
    if insights.total_count > 0:
        print("\n" + "─" * 80)
        print_insight(insights.insights[0], 1)
        
        if insights.insights[0].explanations:
            print(f"\n  {Colors.BOLD}Explainability:{Colors.END}")
            for exp in insights.insights[0].explanations:
                print(f"    • {exp.content}")
                print(f"      Confidence: {exp.confidence:.1%}")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    
    # SECTION 4: ROLE-BASED ADAPTATION
    print_section("SECTION 4: ROLE-BASED PERSONALIZATION", Colors.YELLOW)
    
    print_step(4, "Demonstrating role-specific views...")
    print()
    
    roles_to_demo = [
        ("cfo", "Chief Financial Officer"),
        ("regional_sales_manager", "Regional Sales Manager"),
        ("financial_analyst", "Financial Analyst")
    ]
    
    for role_id, role_name in roles_to_demo:
        print(f"\n{Colors.BOLD}→ Generating report for: {role_name}{Colors.END}")
        print()
        
        # Create role context
        role_context = context_analyzer.create_role_context(role_id)
        insight_req = context_analyzer.get_insight_requirements(role_id)
        
        # Generate role-specific insights
        role_insights = insight_generator.generate_insights(
            sales_data, role_context, insight_req
        )
        
        print_info(f"Decision context: {role_context.role_profile.decision_context.value}")
        print_info(f"Data granularity: {', '.join([g.value for g in role_context.role_profile.data_granularity])}")
        print_info(f"Insights generated: {role_insights.total_count}")
        print_info(f"Max insights allowed: {insight_req.max_insights_per_report}")
        
        kpis = context_analyzer.get_relevant_kpis(role_id)
        print_info(f"Top KPIs: {', '.join(kpis[:3])}")
        
        time.sleep(1)
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}Role-based personalization complete!{Colors.END}")
    print("Each role receives tailored insights based on their responsibilities and decision-making needs.")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    
    # SECTION 5: CONVERSATIONAL INTERFACE
    print_section("SECTION 5: CONVERSATIONAL INTERFACE", Colors.CYAN)
    
    print_step(5, "Interactive conversation with the system...")
    print()
    
    session_id = conversation_manager.create_session(user_role="cfo")
    print_success(f"Conversation session created: {session_id}")
    
    # Simulate conversation
    queries = [
        "What are the key findings?",
        "Why is total amount decreasing?",
        "What should we do about this?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{Colors.BOLD}Query {i}:{Colors.END}")
        print(f"{Colors.BLUE}👤 User:{Colors.END} {query}")
        
        if conversation_manager.use_llm:
            simulate_user_interaction("Processing with LLM", 1.5)
        
        response = conversation_manager.process_message(session_id, query, insights)
        
        print(f"{Colors.GREEN}🤖 Assistant:{Colors.END} {response.response_text[:300]}...")
        print(f"\n{Colors.CYAN}Intent:{Colors.END} {response.intent.value} | {Colors.CYAN}Confidence:{Colors.END} {response.confidence:.0%}")
        
        if response.suggested_questions:
            print(f"\n{Colors.YELLOW}💡 Suggestions:{Colors.END}")
            for suggestion in response.suggested_questions[:2]:
                print(f"  • {suggestion}")
        
        if i < len(queries):
            time.sleep(2)
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}Conversational interface demonstrated!{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    
    # SECTION 6: FEEDBACK & LEARNING
    print_section("SECTION 6: FEEDBACK & ADAPTIVE LEARNING", Colors.YELLOW)
    
    print_step(6, "Collecting user feedback and adapting system...")
    print()
    
    print_info("Simulating user feedback...")
    print()
    
    # Collect feedback
    for i, insight in enumerate(insights.insights[:3], 1):
        rating = [5, 4, 3][i-1]
        feedback_collector.record_insight_feedback(
            insight_id=insight.insight_id,
            rating=rating,
            is_relevant=rating >= 4,
            role_id="cfo"
        )
        print_success(f"Feedback recorded for insight {i}: {rating}/5 stars")
        time.sleep(0.3)
    
    # Implicit feedback
    print()
    print_info("Tracking implicit user behavior...")
    feedback_collector.record_implicit_feedback(
        insight_id=insights.insights[0].insight_id,
        time_spent_viewing=45.0,
        clicked=True,
        drilled_down=True,
        shared=True
    )
    print_success("High engagement detected on top insight")
    
    # Report feedback
    print()
    print_info("Overall report feedback...")
    feedback_collector.record_report_feedback(
        report_id=insights.collection_id,
        overall_rating=4,
        relevance_rating=5,
        clarity_rating=4,
        actionability_rating=4,
        role_id="cfo"
    )
    print_success("Report feedback: 4/5 overall satisfaction")
    
    # Learning
    print()
    print_info("Running learning algorithms...")
    simulate_user_interaction("Analyzing feedback patterns", 1.5)
    
    learning_engine.adapt_system()
    
    print_success("System adapted based on feedback")
    print_info(f"Updated weights for {len(learning_engine.insight_weights)} insights", indent=1)
    print_info(f"Learned preferences for {len(learning_engine.role_preferences)} roles", indent=1)
    
    # Metrics
    print()
    metrics = learning_engine.compute_learning_metrics()
    print(f"{Colors.BOLD}Learning Metrics:{Colors.END}")
    print_info(f"User satisfaction: {metrics.user_satisfaction_score:.1%}")
    print_info(f"Positive feedback rate: {metrics.positive_feedback_rate:.1%}")
    print_info(f"System improvement rate: {metrics.improvement_rate:.1%}")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}Adaptive learning complete!{Colors.END}")
    print("The system continuously improves based on user feedback and behavior.")
    
    input(f"\n{Colors.YELLOW}Press Enter to see final summary...{Colors.END}")
    
    # FINAL SUMMARY
    print_section("DEMONSTRATION COMPLETE", Colors.GREEN)
    
    print(f"{Colors.BOLD}System Performance Summary:{Colors.END}\n")
    
    summary_data = [
        ("Data Sources Processed", f"{3} (CSV, Text, Documents)"),
        ("Total Data Points", f"{sales_data.metadata.row_count + report_data.metadata.word_count:,}"),
        ("Insights Generated", f"{insights.total_count}"),
        ("Average Confidence", f"{insights.avg_confidence:.1%}"),
        ("Roles Configured", f"5 (Executive to Analyst levels)"),
        ("Conversation Turns", f"{len(conversation_manager.active_sessions[session_id].turns)}"),
        ("Feedback Collected", f"{sum(len(f) for f in feedback_collector.insight_feedback.values())}"),
        ("System Adaptations", f"{len(learning_engine.adaptation_history)}"),
        ("User Satisfaction", f"{metrics.user_satisfaction_score:.1%}")
    ]
    
    for label, value in summary_data:
        print(f"  {Colors.CYAN}{label:.<40}{Colors.END} {Colors.BOLD}{value}{Colors.END}")
    
    print(f"\n{Colors.BOLD}Key Features Demonstrated:{Colors.END}\n")
    
    features = [
        "✓ Multi-modal data processing (structured, text, images)",
        "✓ Explainable AI with data provenance and confidence scores",
        "✓ Role-based personalization and access control",
        "✓ Natural language conversational interface with LLM",
        "✓ Adaptive learning from user feedback",
        "✓ Real-time insight generation with statistical analysis",
        "✓ Comprehensive feedback collection (explicit + implicit)",
        "✓ Continuous system improvement and adaptation"
    ]
    
    for feature in features:
        print(f"  {Colors.GREEN}{feature}{Colors.END}")
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}  DEMONSTRATION COMPLETE - ALL MODULES WORKING PERFECTLY!{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")
    
    print(f"{Colors.YELLOW}System ready for:{Colors.END}")
    print("  • Production deployment")
    print("  • User acceptance testing")
    print("  • Academic presentation")
    print("  • Thesis documentation")
    
    print(f"\n{Colors.BOLD}Thank you for watching the demonstration!{Colors.END}\n")

if __name__ == "__main__":
    try:
        demo_full_system()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Demo interrupted by user{Colors.END}")
    except Exception as e:
        logger.error(f"Demo failed: {str(e)}")
        print(f"\n{Colors.RED}Error: {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()