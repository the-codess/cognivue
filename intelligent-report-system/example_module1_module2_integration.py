"""
Integration Example: Module 1 + Module 2
Demonstrates how multi-modal input processing works with role-based filtering
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

from src.modules.input_processing.processor import InputProcessor
from src.modules.role_context.context_analyzer import RoleContextAnalyzer
from src.utils.sample_data_generator import SampleDataGenerator

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def main():
    print_header("MODULE 1 + MODULE 2 INTEGRATION DEMO")
    
    # Initialize
    print("Initializing components...")
    input_processor = InputProcessor()
    context_analyzer = RoleContextAnalyzer()
    generator = SampleDataGenerator()
    print("✓ Components initialized\n")
    
    # Generate and process data with Module 1
    print_header("STEP 1: Multi-Modal Data Processing (Module 1)")
    
    print("Generating sample data files...")
    sales_file = generator.generate_sales_data(num_rows=500)
    report_file = generator.generate_financial_report()
    print(f"✓ Generated sales data: {sales_file}")
    print(f"✓ Generated financial report: {report_file}\n")
    
    print("Processing files...")
    sales_data = input_processor.process_file(sales_file)
    report_data = input_processor.process_file(report_file)
    
    print(f"✓ Sales data processed: {sales_data.metadata.row_count} rows")
    print(f"✓ Report processed: {report_data.metadata.word_count} words")
    print(f"✓ Entities found: {len(report_data.metadata.entities)}")
    print(f"✓ Sentiment: {report_data.metadata.sentiment.label} ({report_data.metadata.sentiment.score:.2f})")
    
    # Apply role-based filtering with Module 2
    print_header("STEP 2: Role-Based Filtering (Module 2)")
    
    # Test with three different roles
    roles_to_test = [
        ("cfo", "Chief Financial Officer"),
        ("regional_sales_manager", "Regional Sales Manager"),
        ("financial_analyst", "Financial Analyst")
    ]
    
    for role_id, role_name in roles_to_test:
        print(f"\n--- {role_name} View ---")
        
        # Create role context
        context = context_analyzer.create_role_context(role_id, time_period="2024-Q3")
        
        # Filter sales data
        filtered_sales = context_analyzer.filter_data_for_role(sales_data, context)
        
        # Get KPIs
        kpis = context_analyzer.get_relevant_kpis(role_id)
        
        # Get insight requirements
        insight_req = context_analyzer.get_insight_requirements(role_id)
        
        # Get visualizations
        viz_prefs = context_analyzer.get_recommended_visualizations(role_id)
        
        print(f"Data Access:")
        print(f"  Rows visible: {filtered_sales.metadata.row_count}")
        print(f"  Columns visible: {filtered_sales.metadata.column_count}")
        
        print(f"\nTop KPIs (showing 3):")
        for kpi in kpis[:3]:
            print(f"  • {kpi}")
        
        print(f"\nInsight Preferences:")
        print(f"  Types: {', '.join(insight_req.insight_types[:3])}...")
        print(f"  Min confidence: {insight_req.min_confidence}")
        print(f"  Max insights: {insight_req.max_insights_per_report}")
        
        print(f"\nVisualization Preferences:")
        for viz in viz_prefs[:2]:
            print(f"  • {viz.replace('_', ' ').title()}")
    
    # Demonstrate data prioritization
    print_header("STEP 3: Intelligent Data Prioritization")
    
    data_items = [sales_data, report_data]
    
    for role_id, role_name in roles_to_test:
        context = context_analyzer.create_role_context(role_id)
        prioritized = context_analyzer.prioritize_data_sources(data_items, context)
        
        print(f"\n{role_name} - Data Priority:")
        for i, item in enumerate(prioritized, 1):
            print(f"  {i}. {item.source_type.value} - {item.modality.value}")
    
    # Summary
    print_header("INTEGRATION SUMMARY")
    
    print("Successfully demonstrated:")
    print("✓ Module 1: Multi-modal data ingestion and processing")
    print("✓ Module 2: Role-based context analysis and filtering")
    print("✓ Integration: Seamless data flow between modules")
    print("\nKey Features:")
    print("• Same data, different views for different roles")
    print("• Automatic KPI mapping based on role")
    print("• Context-aware insight requirements")
    print("• Intelligent data source prioritization")
    print("\nThe system adapts content, granularity, and insights based on")
    print("organizational role, decision context, and access permissions!")
    
    print_header("READY FOR MODULE 3: INSIGHT GENERATION")

if __name__ == "__main__":
    main()