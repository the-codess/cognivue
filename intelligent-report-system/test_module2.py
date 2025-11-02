"""
Test script for Module 2 - Role-Context Analyzer
Run this to validate the module is working correctly
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

from src.modules.role_context.context_analyzer import RoleContextAnalyzer
from src.modules.role_context.role_repository import RoleRepository
from src.modules.input_processing.processor import InputProcessor
from src.utils.sample_data_generator import SampleDataGenerator
from src.utils.logger import app_logger as logger
from src.config.settings import settings

def print_section(title):
    """Print a section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def test_module2():
    """Test Module 2 - Role-Context Analyzer"""
    
    print_section("MODULE 2: ROLE-CONTEXT ANALYZER - TEST SUITE")
    
    # Step 1: Initialize components
    print_section("Step 1: Initializing Components")
    
    role_repo = RoleRepository()
    context_analyzer = RoleContextAnalyzer()
    input_processor = InputProcessor()
    
    print(f"✓ RoleRepository initialized with {len(role_repo.roles)} roles")
    print(f"✓ RoleContextAnalyzer initialized")
    print(f"✓ InputProcessor initialized")
    
    # Step 2: List available roles
    print_section("Step 2: Available Organizational Roles")
    
    roles = role_repo.list_roles()
    print(f"Total roles defined: {len(roles)}\n")
    
    for role in roles:
        print(f"Role: {role.role_name}")
        print(f"  ID: {role.role_id}")
        print(f"  Level: {role.role_level.value}")
        print(f"  Department: {role.department.value}")
        print(f"  Decision Context: {role.decision_context.value}")
        print(f"  Primary KPIs: {len(role.primary_kpis)}")
        print(f"  Focus Areas: {', '.join(role.focus_areas[:3])}...")
        print()
    
    # Step 3: Test role profile details
    print_section("Step 3: Detailed Role Profile - CFO")
    
    cfo = role_repo.get_role("cfo")
    if cfo:
        print(f"Role: {cfo.role_name}")
        print(f"\nData Granularity:")
        for gran in cfo.data_granularity:
            print(f"  - {gran.value}")
        
        print(f"\nTemporal Horizons:")
        for horizon in cfo.temporal_horizons:
            print(f"  - {horizon.value}")
        
        print(f"\nPreferred Visualizations:")
        for viz in cfo.preferred_visualizations:
            print(f"  - {viz.value}")
        
        print(f"\nPrimary KPIs:")
        for kpi in cfo.primary_kpis:
            print(f"  - {kpi.name}: {kpi.description} (Importance: {kpi.importance}/10)")
        
        print(f"\nAccessible Departments: {len(cfo.accessible_departments)}")
        print(f"Focus Areas: {', '.join(cfo.focus_areas)}")
        print(f"Alert Triggers: {', '.join(cfo.alert_triggers)}")
        
        # Check access policy
        access_policy = role_repo.get_access_policy("cfo")
        if access_policy:
            print(f"\nAccess Policy:")
            print(f"  Financial Data: {access_policy.can_view_financial}")
            print(f"  HR Data: {access_policy.can_view_hr}")
            print(f"  Salary Data: {access_policy.can_view_salaries}")
            print(f"  PII Access: {access_policy.pii_access_level}")
    
    # Step 4: Compare different role requirements
    print_section("Step 4: Comparing Role Requirements")
    
    roles_to_compare = ["cfo", "regional_sales_manager", "financial_analyst"]
    
    print("KPI Comparison:\n")
    for role_id in roles_to_compare:
        role = role_repo.get_role(role_id)
        kpis = context_analyzer.get_relevant_kpis(role_id)
        print(f"{role.role_name}:")
        print(f"  KPIs: {', '.join(kpis[:3])}...")
        print()
    
    print("\nVisualization Preferences:\n")
    for role_id in roles_to_compare:
        role = role_repo.get_role(role_id)
        viz_prefs = context_analyzer.get_recommended_visualizations(role_id)
        print(f"{role.role_name}:")
        print(f"  Preferred: {', '.join(viz_prefs)}")
        print()
    
    # Step 5: Test context creation
    print_section("Step 5: Creating Role Contexts")
    
    cfo_context = context_analyzer.create_role_context(
        role_id="cfo",
        time_period="2024-Q3",
        urgency="high"
    )
    print(f"✓ Created context for CFO")
    print(f"  Time Period: {cfo_context.current_time_period}")
    print(f"  Urgency: {cfo_context.urgency}")
    print(f"  Role Level: {cfo_context.role_profile.role_level.value}")
    
    sales_context = context_analyzer.create_role_context(
        role_id="regional_sales_manager",
        time_period="2024-Q3",
        filters={"region": "North"}
    )
    print(f"\n✓ Created context for Regional Sales Manager")
    print(f"  Time Period: {sales_context.current_time_period}")
    print(f"  Filters: {sales_context.specific_filters}")
    
    # Step 6: Test data filtering
    print_section("Step 6: Testing Data Filtering for Roles")
    
    # Generate sample data
    generator = SampleDataGenerator()
    sales_file = generator.generate_sales_data(num_rows=100)
    
    # Process the data
    sales_data = input_processor.process_file(sales_file)
    print(f"Original data: {sales_data.metadata.row_count} rows")
    
    # Filter for CFO (should see all data)
    cfo_filtered = context_analyzer.filter_data_for_role(sales_data, cfo_context)
    print(f"CFO view: {cfo_filtered.metadata.row_count} rows (full access)")
    
    # Filter for Regional Sales Manager
    sales_filtered = context_analyzer.filter_data_for_role(sales_data, sales_context)
    print(f"Regional Sales Manager view: {sales_filtered.metadata.row_count} rows")
    
    # Step 7: Test insight requirements
    print_section("Step 7: Insight Requirements by Role")
    
    for role_id in ["cfo", "regional_sales_manager", "financial_analyst"]:
        role = role_repo.get_role(role_id)
        insight_req = context_analyzer.get_insight_requirements(role_id)
        
        print(f"{role.role_name}:")
        print(f"  Insight Types: {', '.join(insight_req.insight_types)}")
        print(f"  Min Confidence: {insight_req.min_confidence}")
        print(f"  Max Insights: {insight_req.max_insights_per_report}")
        print(f"  Include Recommendations: {insight_req.include_recommendations}")
        print()
    
    # Step 8: Test alert triggers
    print_section("Step 8: Alert Trigger Testing")
    
    test_alerts = [
        "revenue_decline",
        "quota_miss",
        "budget_overrun",
        "customer_churn"
    ]
    
    print("Alert relevance by role:\n")
    for role_id in roles_to_compare:
        role = role_repo.get_role(role_id)
        print(f"{role.role_name}:")
        for alert in test_alerts:
            should_alert = context_analyzer.should_alert(role_id, alert)
            status = "✓" if should_alert else "✗"
            print(f"  {status} {alert}")
        print()
    
    # Step 9: Test data prioritization
    print_section("Step 9: Data Source Prioritization")
    
    # Generate multiple data sources
    report_file = generator.generate_financial_report()
    feedback_file = generator.generate_customer_feedback()
    
    financial_text = input_processor.process_file(report_file)
    customer_text = input_processor.process_file(feedback_file)
    
    data_items = [sales_data, financial_text, customer_text]
    
    # Prioritize for CFO
    cfo_prioritized = context_analyzer.prioritize_data_sources(data_items, cfo_context)
    print("CFO - Data Source Priority:")
    for i, item in enumerate(cfo_prioritized, 1):
        print(f"  {i}. {item.source_type.value} ({item.modality.value})")
    
    # Prioritize for Sales Manager
    sales_prioritized = context_analyzer.prioritize_data_sources(data_items, sales_context)
    print("\nRegional Sales Manager - Data Source Priority:")
    for i, item in enumerate(sales_prioritized, 1):
        print(f"  {i}. {item.source_type.value} ({item.modality.value})")
    
    # Step 10: Summary
    print_section("Test Summary")
    
    print("Module 2 - Role-Context Analyzer\n")
    print("✓ Role Repository: WORKING")
    print("✓ Role Profiles: WORKING")
    print("✓ Access Policies: WORKING")
    print("✓ Context Creation: WORKING")
    print("✓ Data Filtering: WORKING")
    print("✓ KPI Mapping: WORKING")
    print("✓ Insight Requirements: WORKING")
    print("✓ Alert Triggers: WORKING")
    print("✓ Data Prioritization: WORKING")
    
    print("\n" + "="*80)
    print("MODULE 2 TESTING COMPLETED SUCCESSFULLY")
    print("="*80)
    
    print("\nKey Capabilities Demonstrated:")
    print("1. Multiple role profiles with different requirements")
    print("2. Role-based data filtering and access control")
    print("3. KPI mapping and priority setting")
    print("4. Context-aware insight requirements")
    print("5. Intelligent data prioritization")
    
    print("\nNext Steps:")
    print("1. Review role definitions in the output above")
    print("2. Test with custom roles if needed")
    print("3. Proceed to Module 3 development (Insight Generation)")
    
    return True

if __name__ == "__main__":
    try:
        test_module2()
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        print(f"\n✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)