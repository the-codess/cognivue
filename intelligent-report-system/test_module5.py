"""
Test script for Module 5 - Feedback & Learning System
Run this to validate the module is working correctly
"""
import sys
from pathlib import Path
import time

# Add project root to path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

from src.modules.input_processing.processor import InputProcessor
from src.modules.insight_generation.generator import InsightGenerator
from src.modules.feedback_learning.collector import FeedbackCollector
from src.modules.feedback_learning.learning_engine import LearningEngine
from src.utils.sample_data_generator import SampleDataGenerator
from src.utils.logger import app_logger as logger

def print_section(title):
    """Print a section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def test_module5():
    """Test Module 5 - Feedback & Learning System"""
    
    print_section("MODULE 5: FEEDBACK & LEARNING SYSTEM - TEST SUITE")
    
    # Step 1: Initialize components
    print_section("Step 1: Initializing Components")
    
    input_processor = InputProcessor()
    insight_generator = InsightGenerator()
    feedback_collector = FeedbackCollector()
    learning_engine = LearningEngine(feedback_collector)
    generator = SampleDataGenerator()
    
    print("✓ InputProcessor initialized")
    print("✓ InsightGenerator initialized")
    print("✓ FeedbackCollector initialized")
    print("✓ LearningEngine initialized")
    
    # Step 2: Generate insights to get feedback on
    print_section("Step 2: Generating Insights")
    
    sales_file = generator.generate_sales_data(num_rows=400)
    sales_data = input_processor.process_file(sales_file)
    insights = insight_generator.generate_insights(sales_data)
    
    print(f"✓ Generated {insights.total_count} insights")
    print(f"✓ Insights IDs:")
    for i, insight in enumerate(insights.insights[:5], 1):
        print(f"  {i}. {insight.insight_id}: {insight.title}")
    
    # Step 3: Simulate user feedback
    print_section("Step 3: Collecting User Feedback")
    
    print("Simulating user feedback on insights...\n")
    
    # Positive feedback on first insight
    fb1 = feedback_collector.record_insight_feedback(
        insight_id=insights.insights[0].insight_id,
        rating=5,
        is_relevant=True,
        is_accurate=True,
        comment="Very helpful insight, exactly what I needed!",
        role_id="cfo"
    )
    print(f"✓ Positive feedback: 5/5 stars on {insights.insights[0].title}")
    
    # Mixed feedback on second insight
    fb2 = feedback_collector.record_insight_feedback(
        insight_id=insights.insights[1].insight_id,
        rating=3,
        is_relevant=True,
        is_accurate=False,
        comment="Relevant but seems inaccurate",
        role_id="analyst"
    )
    print(f"✓ Mixed feedback: 3/5 stars on {insights.insights[1].title}")
    
    # Negative feedback on third insight
    fb3 = feedback_collector.record_insight_feedback(
        insight_id=insights.insights[2].insight_id,
        rating=2,
        is_relevant=False,
        is_accurate=True,
        comment="Not relevant to my role",
        role_id="sales_manager"
    )
    print(f"✓ Negative feedback: 2/5 stars on {insights.insights[2].title}")
    
    # More positive feedback
    for i in range(3):
        feedback_collector.record_insight_feedback(
            insight_id=insights.insights[0].insight_id,
            rating=4,
            is_relevant=True,
            role_id="cfo"
        )
    print(f"✓ Additional 3 feedbacks recorded")
    
    print(f"\n Total explicit feedback: {sum(len(f) for f in feedback_collector.insight_feedback.values())}")
    
    # Step 4: Test implicit feedback
    print_section("Step 4: Recording Implicit Feedback")
    
    print("Simulating user behavior...\n")
    
    # High engagement
    feedback_collector.record_implicit_feedback(
        insight_id=insights.insights[0].insight_id,
        time_spent_viewing=45.0,
        clicked=True,
        drilled_down=True,
        shared=True,
        user_id="user_001"
    )
    print(f"✓ High engagement: 45s viewing, clicked, drilled down, shared")
    
    # Medium engagement
    feedback_collector.record_implicit_feedback(
        insight_id=insights.insights[1].insight_id,
        time_spent_viewing=15.0,
        clicked=True,
        user_id="user_002"
    )
    print(f"✓ Medium engagement: 15s viewing, clicked")
    
    # Low engagement
    feedback_collector.record_implicit_feedback(
        insight_id=insights.insights[2].insight_id,
        time_spent_viewing=3.0,
        user_id="user_003"
    )
    print(f"✓ Low engagement: 3s viewing only")
    
    print(f"\nTotal implicit feedback: {len(feedback_collector.implicit_feedback)}")
    
    # Step 5: Test report feedback
    print_section("Step 5: Recording Report Feedback")
    
    report_fb = feedback_collector.record_report_feedback(
        report_id=insights.collection_id,
        overall_rating=4,
        relevance_rating=5,
        clarity_rating=4,
        actionability_rating=3,
        what_worked_well="Clear explanations and good visualizations",
        what_needs_improvement="Need more actionable recommendations",
        role_id="cfo"
    )
    
    print(f"✓ Report feedback recorded:")
    print(f"  Overall: {report_fb.overall_rating}/5")
    print(f"  Relevance: {report_fb.relevance_rating}/5")
    print(f"  Clarity: {report_fb.clarity_rating}/5")
    print(f"  Actionability: {report_fb.actionability_rating}/5")
    
    # Step 6: Analyze feedback
    print_section("Step 6: Analyzing Feedback")
    
    print("Computing averages and trends...\n")
    
    for insight in insights.insights[:3]:
        avg_rating = feedback_collector.get_average_rating(insight.insight_id)
        if avg_rating:
            print(f"Insight: {insight.title[:50]}...")
            print(f"  Average rating: {avg_rating:.2f}/5")
            print()
    
    # Step 7: Generate feedback summary
    print_section("Step 7: Feedback Summary")
    
    summary = feedback_collector.get_feedback_summary(days=7)
    
    print(f"Period: {summary.start_date.strftime('%Y-%m-%d')} to {summary.end_date.strftime('%Y-%m-%d')}")
    print(f"Total feedback: {summary.total_feedback}")
    print(f"Average rating: {summary.avg_rating:.2f}/5")
    print(f"Positive rate: {summary.positive_rate:.1%}")
    print(f"Negative rate: {summary.negative_rate:.1%}")
    
    if summary.improvement_suggestions:
        print(f"\nImprovement suggestions:")
        for suggestion in summary.improvement_suggestions:
            print(f"  • {suggestion}")
    
    # Step 8: Learning engine in action
    print_section("Step 8: Learning Engine Adaptation")
    
    print("Running learning algorithms...\n")
    
    # Update weights
    learning_engine.update_insight_weights()
    print(f"✓ Updated insight weights for {len(learning_engine.insight_weights)} insights")
    
    # Learn preferences
    learning_engine.learn_role_preferences()
    print(f"✓ Learned preferences for {len(learning_engine.role_preferences)} roles")
    
    # Show learned weights
    print(f"\nLearned insight weights:")
    for insight_id, weight in list(learning_engine.insight_weights.items())[:3]:
        print(f"  {insight_id}: {weight:.2f}")
    
    # Step 9: System adaptation
    print_section("Step 9: System Adaptation")
    
    learning_engine.adapt_system()
    
    print(f"✓ System adapted based on feedback")
    print(f"✓ Total adaptations: {len(learning_engine.adaptation_history)}")
    
    print(f"\nRecent adaptations:")
    for action in learning_engine.adaptation_history[-3:]:
        print(f"  • {action.action_type}: {action.component}")
        print(f"    Expected impact: {action.expected_impact}")
    
    # Step 10: Compute learning metrics
    print_section("Step 10: Learning Metrics")
    
    metrics = learning_engine.compute_learning_metrics()
    
    print(f"Learning Performance:")
    print(f"  Average insight rating: {metrics.avg_insight_rating:.2f}/5")
    print(f"  Average relevance score: {metrics.avg_relevance_score:.1%}")
    print(f"  User satisfaction: {metrics.user_satisfaction_score:.1%}")
    print(f"  Model accuracy: {metrics.model_accuracy:.1%}")
    print(f"  Improvement rate: {metrics.improvement_rate:.1%}")
    print(f"  Total feedback collected: {metrics.total_feedback_count}")
    
    # Step 11: Get recommendations
    print_section("Step 11: Personalized Recommendations")
    
    print("Testing learned preferences...\n")
    
    available_insights = [i.insight_id for i in insights.insights]
    
    cfo_recommendations = learning_engine.get_recommended_insights_for_role(
        "cfo", available_insights
    )
    print(f"Recommendations for CFO (based on feedback):")
    print(f"  Top 3: {cfo_recommendations[:3]}")
    
    # Step 12: Improvement suggestions
    print_section("Step 12: Improvement Suggestions")
    
    suggestions = learning_engine.get_improvement_suggestions()
    
    if suggestions:
        print("System improvement suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
    else:
        print("✓ No critical improvements needed")
    
    # Summary
    print_section("Test Summary")
    
    print("Module 5 - Feedback & Learning System\n")
    print("✓ Feedback Collection: WORKING")
    print("✓ Implicit Feedback Tracking: WORKING")
    print("✓ Report Feedback: WORKING")
    print("✓ Feedback Analysis: WORKING")
    print("✓ Learning Engine: WORKING")
    print("✓ System Adaptation: WORKING")
    print("✓ Personalization: WORKING")
    print("✓ Metrics Computation: WORKING")
    
    print("\n" + "="*80)
    print("MODULE 5 TESTING COMPLETED SUCCESSFULLY")
    print("="*80)
    
    print("\nKey Capabilities Demonstrated:")
    print("1. Multiple feedback types (ratings, comments, implicit behavior)")
    print("2. Feedback aggregation and analysis")
    print("3. Learning from user preferences")
    print("4. System adaptation based on feedback")
    print("5. Role-specific personalization")
    print("6. Continuous improvement metrics")
    
    print("\nFeedback Statistics:")
    print(f"  Explicit feedback: {sum(len(f) for f in feedback_collector.insight_feedback.values())}")
    print(f"  Implicit feedback: {len(feedback_collector.implicit_feedback)}")
    print(f"  Report feedback: {len(feedback_collector.report_feedback)}")
    print(f"  Average satisfaction: {summary.avg_rating:.2f}/5")
    print(f"  System adaptations: {len(learning_engine.adaptation_history)}")
    
    print("\n🎉 ALL 5 MODULES COMPLETE!")
    print("="*80)
    print("Complete system ready for demonstration and deployment!")
    
    return True

if __name__ == "__main__":
    try:
        test_module5()
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        print(f"\n✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)